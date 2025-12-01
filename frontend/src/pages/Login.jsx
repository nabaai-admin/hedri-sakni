import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authAPI } from '../services/api';
import { toast } from 'react-toastify';
import './Login.css';

export default function Login() {
    const [credentials, setCredentials] = useState({ username: '', password: '' });
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        try {
            const response = await authAPI.login(credentials);
            if (response.data.success) {
                localStorage.setItem('token', response.data.token);
                toast.success('تم تسجيل الدخول بنجاح');
                navigate('/');
            }
        } catch (error) {
            toast.error(error.response?.data?.message || 'فشل تسجيل الدخول');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-container">
            <div className="login-background">
                <div className="login-shape"></div>
                <div className="login-shape"></div>
                <div className="login-shape"></div>
            </div>

            <div className="login-card fade-in">
                <div className="login-header">
                    <div className="login-icon">
                        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M12 2L2 7l10 5 10-5-10-5z" />
                            <path d="M2 17l10 5 10-5M2 12l10 5 10-5" />
                        </svg>
                    </div>
                    <h1>نظام إدارة حجوزات الأراضي</h1>
                    <p>مرحباً بك في لوحة التحكم</p>
                </div>

                <form onSubmit={handleSubmit} className="login-form">
                    <div className="form-group">
                        <label className="label">اسم المستخدم</label>
                        <input
                            type="text"
                            className="input"
                            value={credentials.username}
                            onChange={(e) => setCredentials({ ...credentials, username: e.target.value })}
                            required
                            autoFocus
                            placeholder="أدخل اسم المستخدم"
                        />
                    </div>

                    <div className="form-group">
                        <label className="label">كلمة المرور</label>
                        <input
                            type="password"
                            className="input"
                            value={credentials.password}
                            onChange={(e) => setCredentials({ ...credentials, password: e.target.value })}
                            required
                            placeholder="أدخل كلمة المرور"
                        />
                    </div>

                    <button type="submit" className="btn btn-primary btn-lg" disabled={loading}>
                        {loading ? (
                            <>
                                <span className="spinner-sm"></span>
                                جاري تسجيل الدخول...
                            </>
                        ) : (
                            'تسجيل الدخول'
                        )}
                    </button>
                </form>

                <div className="login-footer">
                    <p>نظام آمن ومحمي</p>
                </div>
            </div>
        </div>
    );
}
