import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { areasAPI, customersAPI, reservationsAPI } from '../services/api';
import { toast } from 'react-toastify';
import './Management.css';

export default function Management() {
    const [activeTab, setActiveTab] = useState('customers');
    const queryClient = useQueryClient();

    return (
        <div className="management fade-in">
            <div className="page-header">
                <h1>إدارة البيانات</h1>
                <p>إدارة المناطق والعملاء ومواعيد الحجز</p>
            </div>

            <div className="tabs">
                <button
                    className={`tab ${activeTab === 'customers' ? 'active' : ''}`}
                    onClick={() => setActiveTab('customers')}
                >
                    العملاء
                </button>
                <button
                    className={`tab ${activeTab === 'areas' ? 'active' : ''}`}
                    onClick={() => setActiveTab('areas')}
                >
                    المناطق
                </button>
                <button
                    className={`tab ${activeTab === 'reservations' ? 'active' : ''}`}
                    onClick={() => setActiveTab('reservations')}
                >
                    مواعيد الحجز
                </button>
            </div>

            <div className="tab-content">
                {activeTab === 'customers' && <CustomersTab />}
                {activeTab === 'areas' && <AreasTab />}
                {activeTab === 'reservations' && <ReservationsTab />}
            </div>
        </div>
    );
}

function CustomersTab() {
    const [showForm, setShowForm] = useState(false);
    const [editingCustomer, setEditingCustomer] = useState(null);
    const queryClient = useQueryClient();

    const { data: customers, isLoading } = useQuery({
        queryKey: ['customers'],
        queryFn: () => customersAPI.getAll().then(res => res.data.data)
    });

    const { data: areas } = useQuery({
        queryKey: ['areas'],
        queryFn: () => areasAPI.getAll({ is_active: true }).then(res => res.data.data)
    });

    const deleteMutation = useMutation({
        mutationFn: (id) => customersAPI.delete(id),
        onSuccess: () => {
            queryClient.invalidateQueries(['customers']);
            toast.success('تم حذف العميل بنجاح');
        },
        onError: () => toast.error('فشل حذف العميل')
    });

    if (isLoading) {
        return <div className="loading"><div className="spinner"></div></div>;
    }

    return (
        <div className="tab-panel">
            <div className="panel-header">
                <h2>قائمة العملاء</h2>
                <button className="btn btn-primary" onClick={() => setShowForm(true)}>
                    <span>+</span> إضافة عميل جديد
                </button>
            </div>

            {showForm && (
                <CustomerForm
                    customer={editingCustomer}
                    areas={areas}
                    onClose={() => {
                        setShowForm(false);
                        setEditingCustomer(null);
                    }}
                />
            )}

            <div className="table-container">
                <table className="table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>الاسم</th>
                            <th>رقم الهاتف</th>
                            <th>الرقم الوطني</th>
                            <th>المنطقة</th>
                            <th>حالة الحجز</th>
                            <th>الإجراءات</th>
                        </tr>
                    </thead>
                    <tbody>
                        {customers?.map((customer) => (
                            <tr key={customer.id}>
                                <td>{customer.id}</td>
                                <td>{customer.name}</td>
                                <td>{customer.phone_number}</td>
                                <td>{customer.national_id}</td>
                                <td>{customer.area_name}</td>
                                <td>
                                    <span className={`badge badge-${customer.reservation_status === 'SUCCESS' ? 'success' :
                                        customer.reservation_status === 'FAILED' ? 'danger' : 'warning'
                                        }`}>
                                        {customer.reservation_status === 'SUCCESS' ? 'ناجح' :
                                            customer.reservation_status === 'FAILED' ? 'فاشل' : 'قيد الانتظار'}
                                    </span>
                                </td>
                                <td>
                                    <div className="action-buttons">
                                        <button
                                            className="btn btn-sm btn-secondary"
                                            onClick={() => {
                                                setEditingCustomer(customer);
                                                setShowForm(true);
                                            }}
                                        >
                                            تعديل
                                        </button>
                                        <button
                                            className="btn btn-sm btn-danger"
                                            onClick={() => {
                                                if (confirm('هل أنت متأكد من حذف هذا العميل؟')) {
                                                    deleteMutation.mutate(customer.id);
                                                }
                                            }}
                                        >
                                            حذف
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}

function CustomerForm({ customer, areas, onClose }) {
    const [formData, setFormData] = useState(customer || {
        name: '',
        phone_number: '',
        national_id: '',
        area_id: '',
        reservation_status: 'OPEN'
    });
    const queryClient = useQueryClient();

    const mutation = useMutation({
        mutationFn: (data) => customer
            ? customersAPI.update(customer.id, data)
            : customersAPI.create(data),
        onSuccess: () => {
            queryClient.invalidateQueries(['customers']);
            toast.success(customer ? 'تم تحديث العميل بنجاح' : 'تم إضافة العميل بنجاح');
            onClose();
        },
        onError: (error) => {
            toast.error(error.response?.data?.message || 'حدث خطأ');
        }
    });

    const handleSubmit = (e) => {
        e.preventDefault();
        mutation.mutate(formData);
    };

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                <div className="modal-header">
                    <h3>{customer ? 'تعديل العميل' : 'إضافة عميل جديد'}</h3>
                    <button className="close-btn" onClick={onClose}>×</button>
                </div>

                <form onSubmit={handleSubmit} className="form">
                    <div className="form-group">
                        <label className="label">الاسم</label>
                        <input
                            type="text"
                            className="input"
                            value={formData.name}
                            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label className="label">رقم الهاتف</label>
                        <input
                            type="tel"
                            className="input"
                            value={formData.phone_number}
                            onChange={(e) => setFormData({ ...formData, phone_number: e.target.value })}
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label className="label">الرقم الوطني</label>
                        <input
                            type="text"
                            className="input"
                            value={formData.national_id}
                            onChange={(e) => setFormData({ ...formData, national_id: e.target.value })}
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label className="label">المنطقة</label>
                        <select
                            className="select"
                            value={formData.area_id}
                            onChange={(e) => setFormData({ ...formData, area_id: parseInt(e.target.value) })}
                            required
                        >
                            <option value="">اختر المنطقة</option>
                            {areas?.map((area) => (
                                <option key={area.id} value={area.id}>{area.name}</option>
                            ))}
                        </select>
                    </div>

                    <div className="form-group">
                        <label className="label">حالة الحجز</label>
                        <select
                            className="select"
                            value={formData.reservation_status}
                            onChange={(e) => setFormData({ ...formData, reservation_status: e.target.value })}
                        >
                            <option value="OPEN">قيد الانتظار</option>
                            <option value="SUCCESS">ناجح</option>
                            <option value="FAILED">فاشل</option>
                        </select>
                    </div>

                    <div className="form-actions">
                        <button type="submit" className="btn btn-primary" disabled={mutation.isPending}>
                            {mutation.isPending ? 'جاري الحفظ...' : 'حفظ'}
                        </button>
                        <button type="button" className="btn btn-secondary" onClick={onClose}>
                            إلغاء
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}

function AreasTab() {
    const [showForm, setShowForm] = useState(false);
    const [editingArea, setEditingArea] = useState(null);
    const queryClient = useQueryClient();

    const { data: areas, isLoading } = useQuery({
        queryKey: ['areas'],
        queryFn: () => areasAPI.getAll().then(res => res.data.data)
    });

    const deleteMutation = useMutation({
        mutationFn: (id) => areasAPI.delete(id),
        onSuccess: () => {
            queryClient.invalidateQueries(['areas']);
            toast.success('تم حذف المنطقة بنجاح');
        },
        onError: () => toast.error('فشل حذف المنطقة')
    });

    if (isLoading) {
        return <div className="loading"><div className="spinner"></div></div>;
    }

    return (
        <div className="tab-panel">
            <div className="panel-header">
                <h2>قائمة المناطق</h2>
                <button className="btn btn-primary" onClick={() => setShowForm(true)}>
                    <span>+</span> إضافة منطقة جديدة
                </button>
            </div>

            {showForm && (
                <AreaForm
                    area={editingArea}
                    onClose={() => {
                        setShowForm(false);
                        setEditingArea(null);
                    }}
                />
            )}

            <div className="table-container">
                <table className="table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>اسم المنطقة</th>
                            <th>الرابط</th>
                            <th>الوصف</th>
                            <th>الحالة</th>
                            <th>تاريخ الإنشاء</th>
                            <th>الإجراءات</th>
                        </tr>
                    </thead>
                    <tbody>
                        {areas?.map((area) => (
                            <tr key={area.id}>
                                <td>{area.id}</td>
                                <td>{area.name}</td>
                                <td>
                                    {area.link ? (
                                        <a href={area.link} target="_blank" rel="noopener noreferrer" className="text-primary">
                                            رابط
                                        </a>
                                    ) : '-'}
                                </td>
                                <td>{area.description || '-'}</td>
                                <td>
                                    <span className={`badge badge-${area.is_active ? 'success' : 'danger'}`}>
                                        {area.is_active ? 'نشط' : 'غير نشط'}
                                    </span>
                                </td>
                                <td>{new Date(area.created_at).toLocaleDateString('ar-SA')}</td>
                                <td>
                                    <div className="action-buttons">
                                        <button
                                            className="btn btn-sm btn-secondary"
                                            onClick={() => {
                                                setEditingArea(area);
                                                setShowForm(true);
                                            }}
                                        >
                                            تعديل
                                        </button>
                                        <button
                                            className="btn btn-sm btn-danger"
                                            onClick={() => {
                                                if (confirm('هل أنت متأكد من حذف هذه المنطقة؟')) {
                                                    deleteMutation.mutate(area.id);
                                                }
                                            }}
                                        >
                                            حذف
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}

function AreaForm({ area, onClose }) {
    const [formData, setFormData] = useState(area || {
        name: '',
        description: '',
        link: '',
        is_active: true
    });
    const queryClient = useQueryClient();

    const mutation = useMutation({
        mutationFn: (data) => area
            ? areasAPI.update(area.id, data)
            : areasAPI.create(data),
        onSuccess: () => {
            queryClient.invalidateQueries(['areas']);
            toast.success(area ? 'تم تحديث المنطقة بنجاح' : 'تم إضافة المنطقة بنجاح');
            onClose();
        },
        onError: (error) => {
            toast.error(error.response?.data?.message || 'حدث خطأ');
        }
    });

    const handleSubmit = (e) => {
        e.preventDefault();
        mutation.mutate(formData);
    };

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                <div className="modal-header">
                    <h3>{area ? 'تعديل المنطقة' : 'إضافة منطقة جديدة'}</h3>
                    <button className="close-btn" onClick={onClose}>×</button>
                </div>

                <form onSubmit={handleSubmit} className="form">
                    <div className="form-group">
                        <label className="label">اسم المنطقة</label>
                        <input
                            type="text"
                            className="input"
                            value={formData.name}
                            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                            required
                            placeholder="مثال: الرياض، جدة، الدمام"
                        />
                    </div>

                    <div className="form-group">
                        <label className="label">رابط المنطقة (اختياري)</label>
                        <input
                            type="url"
                            className="input"
                            value={formData.link || ''}
                            onChange={(e) => setFormData({ ...formData, link: e.target.value })}
                            placeholder="https://..."
                        />
                    </div>

                    <div className="form-group">
                        <label className="label">الوصف (اختياري)</label>
                        <textarea
                            className="input"
                            rows="3"
                            value={formData.description}
                            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                            placeholder="وصف المنطقة..."
                        />
                    </div>

                    <div className="form-group">
                        <label className="label">
                            <input
                                type="checkbox"
                                checked={formData.is_active}
                                onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
                                style={{ marginLeft: '8px' }}
                            />
                            منطقة نشطة
                        </label>
                    </div>

                    <div className="form-actions">
                        <button type="submit" className="btn btn-primary" disabled={mutation.isPending}>
                            {mutation.isPending ? 'جاري الحفظ...' : 'حفظ'}
                        </button>
                        <button type="button" className="btn btn-secondary" onClick={onClose}>
                            إلغاء
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}

function ReservationsTab() {
    const [showForm, setShowForm] = useState(false);
    const [editingSlot, setEditingSlot] = useState(null);
    const queryClient = useQueryClient();

    const { data: slots, isLoading } = useQuery({
        queryKey: ['reservations'],
        queryFn: () => reservationsAPI.getAll().then(res => res.data.data)
    });

    const { data: areas } = useQuery({
        queryKey: ['areas'],
        queryFn: () => areasAPI.getAll({ is_active: true }).then(res => res.data.data)
    });

    const deleteMutation = useMutation({
        mutationFn: (id) => reservationsAPI.delete(id),
        onSuccess: () => {
            queryClient.invalidateQueries(['reservations']);
            toast.success('تم حذف موعد الحجز بنجاح');
        },
        onError: (error) => {
            toast.error(error.response?.data?.message || 'فشل حذف موعد الحجز');
        }
    });

    if (isLoading) {
        return <div className="loading"><div className="spinner"></div></div>;
    }

    return (
        <div className="tab-panel">
            <div className="panel-header">
                <h2>قائمة مواعيد الحجز</h2>
                <button className="btn btn-primary" onClick={() => setShowForm(true)}>
                    <span>+</span> إضافة موعد جديد
                </button>
            </div>

            {showForm && (
                <ReservationForm
                    slot={editingSlot}
                    areas={areas}
                    onClose={() => {
                        setShowForm(false);
                        setEditingSlot(null);
                    }}
                />
            )}

            <div className="table-container">
                <table className="table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>المنطقة</th>
                            <th>التاريخ والوقت</th>
                            <th>الحالة</th>
                            <th>تاريخ الإنشاء</th>
                            <th>الإجراءات</th>
                        </tr>
                    </thead>
                    <tbody>
                        {slots?.map((slot) => (
                            <tr key={slot.id}>
                                <td>{slot.id}</td>
                                <td>{slot.area_name}</td>
                                <td>
                                    {new Date(slot.scheduled_datetime).toLocaleString('ar-SA', {
                                        year: 'numeric',
                                        month: 'long',
                                        day: 'numeric',
                                        hour: '2-digit',
                                        minute: '2-digit'
                                    })}
                                </td>
                                <td>
                                    <span className={`badge badge-${slot.is_processed ? 'success' : 'warning'}`}>
                                        {slot.is_processed ? 'تم التنفيذ' : 'قيد الانتظار'}
                                    </span>
                                </td>
                                <td>{new Date(slot.created_at).toLocaleDateString('ar-SA')}</td>
                                <td>
                                    <div className="action-buttons">
                                        {!slot.is_processed && (
                                            <>
                                                <button
                                                    className="btn btn-sm btn-secondary"
                                                    onClick={() => {
                                                        setEditingSlot(slot);
                                                        setShowForm(true);
                                                    }}
                                                >
                                                    تعديل
                                                </button>
                                                <button
                                                    className="btn btn-sm btn-danger"
                                                    onClick={() => {
                                                        if (confirm('هل أنت متأكد من حذف هذا الموعد؟')) {
                                                            deleteMutation.mutate(slot.id);
                                                        }
                                                    }}
                                                >
                                                    حذف
                                                </button>
                                            </>
                                        )}
                                        {slot.is_processed && (
                                            <span style={{ color: 'var(--neutral-500)', fontSize: 'var(--font-size-sm)' }}>
                                                تم التنفيذ
                                            </span>
                                        )}
                                    </div>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}

function ReservationForm({ slot, areas, onClose }) {
    const [formData, setFormData] = useState(() => {
        if (slot) {
            // Convert ISO datetime to local datetime-local format
            const date = new Date(slot.scheduled_datetime);
            const localDateTime = new Date(date.getTime() - date.getTimezoneOffset() * 60000)
                .toISOString()
                .slice(0, 16);
            return {
                area_id: slot.area_id,
                scheduled_datetime: localDateTime
            };
        }
        return {
            area_id: '',
            scheduled_datetime: ''
        };
    });
    const queryClient = useQueryClient();

    const mutation = useMutation({
        mutationFn: (data) => {
            // Convert local datetime to ISO format
            const isoDateTime = new Date(data.scheduled_datetime).toISOString();
            const payload = {
                ...data,
                scheduled_datetime: isoDateTime
            };
            return slot
                ? reservationsAPI.update(slot.id, payload)
                : reservationsAPI.create(payload);
        },
        onSuccess: () => {
            queryClient.invalidateQueries(['reservations']);
            toast.success(slot ? 'تم تحديث الموعد بنجاح' : 'تم إضافة الموعد بنجاح');
            onClose();
        },
        onError: (error) => {
            toast.error(error.response?.data?.message || 'حدث خطأ');
        }
    });

    const handleSubmit = (e) => {
        e.preventDefault();

        // Validate datetime is in the future
        const selectedDate = new Date(formData.scheduled_datetime);
        const now = new Date();

        if (selectedDate <= now) {
            toast.error('يجب أن يكون التاريخ والوقت في المستقبل');
            return;
        }

        mutation.mutate(formData);
    };

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                <div className="modal-header">
                    <h3>{slot ? 'تعديل موعد الحجز' : 'إضافة موعد حجز جديد'}</h3>
                    <button className="close-btn" onClick={onClose}>×</button>
                </div>

                <form onSubmit={handleSubmit} className="form">
                    <div className="form-group">
                        <label className="label">المنطقة</label>
                        <select
                            className="select"
                            value={formData.area_id}
                            onChange={(e) => setFormData({ ...formData, area_id: parseInt(e.target.value) })}
                            required
                        >
                            <option value="">اختر المنطقة</option>
                            {areas?.map((area) => (
                                <option key={area.id} value={area.id}>{area.name}</option>
                            ))}
                        </select>
                    </div>

                    <div className="form-group">
                        <label className="label">التاريخ والوقت</label>
                        <input
                            type="datetime-local"
                            className="input"
                            value={formData.scheduled_datetime}
                            onChange={(e) => setFormData({ ...formData, scheduled_datetime: e.target.value })}
                            required
                        />
                        <small style={{ color: 'var(--neutral-600)', fontSize: 'var(--font-size-sm)', marginTop: '4px', display: 'block' }}>
                            سيتم إرسال طلبات الحجز تلقائياً في الوقت المحدد
                        </small>
                    </div>

                    <div className="form-actions">
                        <button type="submit" className="btn btn-primary" disabled={mutation.isPending}>
                            {mutation.isPending ? 'جاري الحفظ...' : 'حفظ وجدولة'}
                        </button>
                        <button type="button" className="btn btn-secondary" onClick={onClose}>
                            إلغاء
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}

