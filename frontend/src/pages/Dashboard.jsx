import { useQuery } from '@tanstack/react-query';
import { analyticsAPI } from '../services/api';
import './Dashboard.css';

export default function Dashboard() {
    const { data: summary, isLoading } = useQuery({
        queryKey: ['analytics-summary'],
        queryFn: () => analyticsAPI.getSummary().then(res => res.data.data)
    });

    if (isLoading) {
        return (
            <div className="loading">
                <div className="spinner"></div>
            </div>
        );
    }

    const stats = [
        {
            title: 'إجمالي المحاولات',
            value: summary?.total_attempts || 0,
            icon: '📊',
            color: 'primary'
        },
        {
            title: 'الحجوزات الناجحة',
            value: summary?.success_count || 0,
            icon: '✅',
            color: 'success'
        },
        {
            title: 'الحجوزات الفاشلة',
            value: summary?.failed_count || 0,
            icon: '❌',
            color: 'danger'
        },
        {
            title: 'قيد الانتظار',
            value: summary?.open_count || 0,
            icon: '⏳',
            color: 'warning'
        }
    ];

    return (
        <div className="dashboard fade-in">
            <div className="page-header">
                <h1>لوحة التحكم</h1>
                <p>نظرة عامة على حجوزات الأراضي</p>
            </div>

            <div className="stats-grid">
                {stats.map((stat, index) => (
                    <div key={index} className={`stat-card stat-${stat.color}`}>
                        <div className="stat-icon">{stat.icon}</div>
                        <div className="stat-content">
                            <h3>{stat.title}</h3>
                            <p className="stat-value">{stat.value}</p>
                        </div>
                    </div>
                ))}
            </div>

            <div className="dashboard-grid">
                <div className="card">
                    <h2>معدل النجاح</h2>
                    <div className="success-rate">
                        <div className="rate-circle">
                            <svg viewBox="0 0 100 100">
                                <circle cx="50" cy="50" r="45" fill="none" stroke="var(--neutral-200)" strokeWidth="10" />
                                <circle
                                    cx="50"
                                    cy="50"
                                    r="45"
                                    fill="none"
                                    stroke="url(#gradient)"
                                    strokeWidth="10"
                                    strokeDasharray={`${(summary?.success_rate || 0) * 2.827} 282.7`}
                                    strokeLinecap="round"
                                    transform="rotate(-90 50 50)"
                                />
                                <defs>
                                    <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                                        <stop offset="0%" stopColor="var(--primary)" />
                                        <stop offset="100%" stopColor="var(--secondary)" />
                                    </linearGradient>
                                </defs>
                            </svg>
                            <div className="rate-text">
                                <span className="rate-number">{summary?.success_rate || 0}%</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="card">
                    <h2>الإحصائيات حسب المنطقة</h2>
                    <div className="area-stats">
                        {summary?.by_area?.slice(0, 5).map((area, index) => (
                            <div key={index} className="area-item">
                                <div className="area-info">
                                    <span className="area-name">{area.area_name}</span>
                                    <span className="area-count">{area.total} محاولة</span>
                                </div>
                                <div className="area-bar">
                                    <div
                                        className="area-bar-fill"
                                        style={{ width: `${area.success_rate}%` }}
                                    ></div>
                                </div>
                                <span className="area-rate">{area.success_rate.toFixed(1)}%</span>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}
