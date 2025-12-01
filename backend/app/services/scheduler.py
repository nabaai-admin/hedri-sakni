from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from datetime import datetime
import logging
from typing import Optional

from app.models import db, ReservationSlot, Customer, ReservationAttempt
from app.services.uipath_client import UiPathClient

logger = logging.getLogger(__name__)


class ReservationScheduler:
    """Manages scheduling and execution of reservation requests"""
    
    def __init__(self, app=None):
        self.scheduler = BackgroundScheduler()
        self.uipath_client: Optional[UiPathClient] = None
        self.app = app
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize scheduler with Flask app"""
        self.app = app
        
        # Initialize UiPath client
        self.uipath_client = UiPathClient(
            api_url=app.config['UIPATH_API_URL'],
            api_key=app.config['UIPATH_API_KEY'],
            client_id=app.config['UIPATH_CLIENT_ID'],
            client_secret=app.config['UIPATH_CLIENT_SECRET']
        )
        
        # Configure scheduler
        self.scheduler.configure(timezone=app.config['SCHEDULER_TIMEZONE'])
        
        # Start scheduler
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("Reservation scheduler started")
    
    def schedule_reservation_slot(self, slot_id: int, scheduled_datetime: datetime):
        """
        Schedule a reservation slot to be processed at the specified time
        
        Args:
            slot_id: ID of the reservation slot
            scheduled_datetime: When to process the reservation
        """
        job_id = f"reservation_slot_{slot_id}"
        
        # Remove existing job if any
        if self.scheduler.get_job(job_id):
            self.scheduler.remove_job(job_id)
        
        # Schedule new job
        self.scheduler.add_job(
            func=self._process_reservation_slot,
            trigger=DateTrigger(run_date=scheduled_datetime),
            args=[slot_id],
            id=job_id,
            name=f"Process Reservation Slot {slot_id}",
            misfire_grace_time=300,  # 5 minutes grace period
            replace_existing=True
        )
        
        logger.info(f"Scheduled reservation slot {slot_id} for {scheduled_datetime}")
    
    def _process_reservation_slot(self, slot_id: int):
        """
        Process a reservation slot by sending requests for all customers in that area
        
        Args:
            slot_id: ID of the reservation slot to process
        """
        with self.app.app_context():
            try:
                # Get the reservation slot
                slot = ReservationSlot.query.get(slot_id)
                if not slot:
                    logger.error(f"Reservation slot {slot_id} not found")
                    return
                
                if slot.is_processed:
                    logger.warning(f"Reservation slot {slot_id} already processed")
                    return
                
                # Get all customers with OPEN status for this area
                customers = Customer.query.filter_by(
                    area_id=slot.area_id,
                    reservation_status='OPEN'
                ).all()
                
                logger.info(f"Processing {len(customers)} customers for slot {slot_id}, area: {slot.area.name}")
                
                # Process each customer
                for customer in customers:
                    self._send_reservation_request(customer, slot)
                
                # Mark slot as processed
                slot.is_processed = True
                db.session.commit()
                
                logger.info(f"Completed processing reservation slot {slot_id}")
                
            except Exception as e:
                logger.error(f"Error processing reservation slot {slot_id}: {str(e)}")
                db.session.rollback()
    
    def _send_reservation_request(self, customer: Customer, slot: ReservationSlot):
        """
        Send reservation request for a single customer
        
        Args:
            customer: Customer to process
            slot: Reservation slot
        """
        try:
            # Create reservation attempt record
            attempt = ReservationAttempt(
                customer_id=customer.id,
                reservation_slot_id=slot.id,
                request_sent_at=datetime.utcnow(),
                request_payload={
                    'national_id': customer.national_id,
                    'phone_number': customer.phone_number,
                    'area': slot.area.name
                }
            )
            db.session.add(attempt)
            db.session.flush()  # Get the attempt ID
            
            # Send request to UiPath
            response = self.uipath_client.send_reservation_request(
                national_id=customer.national_id,
                phone_number=customer.phone_number,
                area=slot.area.name
            )
            
            # Update attempt with response (if immediate response)
            # Note: The actual status update will come via webhook
            attempt.response_payload = response.get('data', {})
            
            db.session.commit()
            
            logger.info(f"Sent reservation request for customer {customer.id} (national_id: {customer.national_id})")
            
        except Exception as e:
            logger.error(f"Error sending reservation request for customer {customer.id}: {str(e)}")
            db.session.rollback()
    
    def reschedule_all_pending_slots(self):
        """Reschedule all pending (non-processed) reservation slots on app startup"""
        with self.app.app_context():
            try:
                pending_slots = ReservationSlot.query.filter_by(is_processed=False).all()
                
                now = datetime.utcnow()
                for slot in pending_slots:
                    if slot.scheduled_datetime > now:
                        self.schedule_reservation_slot(slot.id, slot.scheduled_datetime)
                    else:
                        logger.warning(f"Slot {slot.id} scheduled time has passed, skipping")
                
                logger.info(f"Rescheduled {len(pending_slots)} pending reservation slots")
                
            except Exception as e:
                logger.error(f"Error rescheduling pending slots: {str(e)}")
    
    def shutdown(self):
        """Shutdown the scheduler gracefully"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Reservation scheduler shut down")


# Global scheduler instance
reservation_scheduler = ReservationScheduler()
