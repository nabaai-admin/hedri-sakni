import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { analyticsAPI, areasAPI } from '../services/api';
import { format } from 'date-fns';
import './Analytics.css';

export default function Analytics() {
    const [filters, setFilters] = useState({
        area_id: '',
        status: '',
        start_date: '',
        end_date: ''
    });

    const { data: summary } = useQuery({
        queryKey: ['analytics-summary', filters],
        queryFn: () => analyticsAPI.getSummary(filters).then(res => res.data.data)
    });

    const { data: attempts, isLoading } = useQuery({
        queryKey: ['analytics-attempts', filters],
        queryFn: () => analyticsAPI.getAttempts(filters).then(res => res.data.data)
    });

    const { data: areas } = useQuery({
        queryKey: ['areas'],
        queryFn: () => areasAPI.getAll().then(res => res.data.data)
    });

    return (
        <div className="analytics fade-in">
            <div className="page-header">
                <h1>التقارير والتحليلات</h1>
                <p>تحليل شامل لنتائج الحجوزات</p>
            </div>

            <div className="filters-card card">
                <h3>الفلاتر</h3>
                <div className="filters-grid">
                    <div className="form-group">
                        <label className="label">المنطقة</label>
                        <select
                            className="select"
                            value={filters.area_id}
                            onChange={(e) => setFilters({ ...filters, area_id: e.target.value })}
                        >
                            <option value="">جميع المناطق</option>
                            {areas?.map((area) => (
                                <option key={area.id} value={area.id}>{area.name}</option>
                            ))}
                        </select>
                    </div>

                    <div className="form-group">
                        <label className="label">الحالة</label>
                        <select
                            className="select"
                            value={filters.status}
                            onChange={(e) => setFilters({ ...filters, status: e.target.value })}
                        >
                            <option value="">جميع الحالات</option>
                            <option value="SUCCESS">ناجح</option>
                            <option value="FAILED">فاشل</option>
                        </select>
                    </div>

                    <div className="form-group">
                        <label className="label">من تاريخ</label>
                        <input
                            type="date"
                            className="input"
                            value={filters.start_date}
                            onChange={(e) => setFilters({ ...filters, start_date: e.target.value })}
                        />
                    </div>

                    <div className="form-group">
                        <label className="label">إلى تاريخ</label>
                        <input
                            type="date"
                            className="input"
                            value={filters.end_date}
                            onChange={(e) => setFilters({ ...filters, end_date: e.target.value })}
                        />
                    </div>
                </div>

                <button
                    className="btn btn-secondary"
                    onClick={() => setFilters({ area_id: '', status: '', start_date: '', end_date: '' })}
                >
                    إعادة تعيين الفلاتر
                </button>
            </div>

            <div className="summary-grid">
                <div className="summary-card">
                    <div className="summary-icon" style={{ background: 'var(--primary-light)' }}>📊</div>
                    <div className="summary-content">
                        <h4>إجمالي المحاولات</h4>
                        <p className="summary-value">{summary?.total_attempts || 0}</p>
                    </div>
                </div>

                <div className="summary-card">
                    <div className="summary-icon" style={{ background: 'var(--success-light)' }}>✅</div>
                    <div className="summary-content">
                        <h4>الحجوزات الناجحة</h4>
                        <p className="summary-value">{summary?.success_count || 0}</p>
                    </div>
                </div>

                <div className="summary-card">
                    <div className="summary-icon" style={{ background: 'var(--danger-light)' }}>❌</div>
                    <div className="summary-content">
                        <h4>الحجوزات الفاشلة</h4>
                        <p className="summary-value">{summary?.failed_count || 0}</p>
                    </div>
                </div>

                <div className="summary-card">
                    <div className="summary-icon" style={{ background: 'var(--warning-light)' }}>📈</div>
                    <div className="summary-content">
                        <h4>معدل النجاح</h4>
                        <p className="summary-value">{summary?.success_rate || 0}%</p>
                    </div>
                </div>
            </div>

            <div className="card">
                <h2>الإحصائيات حسب المنطقة</h2>
                <div className="area-analytics">
                    {summary?.by_area?.map((area, index) => (
                        <div key={index} className="area-analytics-item">
                            <div className="area-analytics-header">
                                <h4>{area.area_name}</h4>
                                <span className="area-total">{area.total} محاولة</span>
                            </div>
                            <div className="area-analytics-stats">
                                <div className="stat-item success">
                                    <span className="stat-label">ناجح</span>
                                    <span className="stat-number">{area.success}</span>
                                </div>
                                <div className="stat-item failed">
                                    <span className="stat-label">فاشل</span>
                                    <span className="stat-number">{area.failed}</span>
                                </div>
                                <div className="stat-item open">
                                    <span className="stat-label">قيد الانتظار</span>
                                    <span className="stat-number">{area.open}</span>
                                </div>
                            </div>
                            <div className="area-progress">
                                <div className="progress-bar">
                                    <div
                                        className="progress-fill"
                                        style={{ width: `${area.success_rate}%` }}
                                    ></div>
                                </div>
                                <span className="progress-label">{area.success_rate.toFixed(1)}%</span>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            <div className="card">
                <h2>سجل المحاولات التفصيلي</h2>
                {isLoading ? (
                    <div className="loading"><div className="spinner"></div></div>
                ) : (
                    <div className="table-container">
                        <table className="table">
                            <thead>
                                <tr>
                                    <th>اسم العميل</th>
                                    <th>الرقم الوطني</th>
                                    <th>المنطقة</th>
                                    <th>تاريخ المحاولة</th>
                                    <th>الحالة</th>
                                    <th>رمز الاستجابة</th>
                                    <th>الرسالة</th>
                                </tr>
                            </thead>
                            <tbody>
                                {attempts?.map((attempt) => (
                                    <tr key={attempt.id}>
                                        <td>{attempt.customer_name}</td>
                                        <td>{attempt.customer_national_id}</td>
                                        <td>{attempt.area_name}</td>
                                        <td>
                                            {attempt.request_sent_at
                                                ? format(new Date(attempt.request_sent_at), 'yyyy-MM-dd HH:mm')
                                                : '-'}
                                        </td>
                                        <td>
                                            <span className={`badge badge-${attempt.response_status === 'SUCCESS' ? 'success' : 'danger'
                                                }`}>
                                                {attempt.response_status === 'SUCCESS' ? 'ناجح' : 'فاشل'}
                                            </span>
                                        </td>
                                        <td>{attempt.response_code || '-'}</td>
                                        <td className="message-cell">{attempt.response_message || '-'}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>
        </div>
    );
}
