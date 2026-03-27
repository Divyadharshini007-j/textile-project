import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

// ── Main app API (uses 'token') ──────────────────────────────────────────────
const mainApi = axios.create({ baseURL: API_BASE_URL });
mainApi.interceptors.request.use(config => {
    const token = localStorage.getItem('token');
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
});

// ── Worker API (uses 'worker_token') ─────────────────────────────────────────
const workerApi = axios.create({ baseURL: API_BASE_URL });
workerApi.interceptors.request.use(config => {
    const token = localStorage.getItem('worker_token');
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
});
workerApi.interceptors.response.use(
    res => res,
    err => {
        if (err.response?.status === 401) {
            localStorage.removeItem('worker_token');
            localStorage.removeItem('worker_user');
            window.location.href = '/worker/login';
        }
        return Promise.reject(err);
    }
);

// ── Admin Hiring API (uses 'admin_hiring_token') ──────────────────────────────
const adminHiringApi = axios.create({ baseURL: API_BASE_URL });
adminHiringApi.interceptors.request.use(config => {
    const token = localStorage.getItem('admin_hiring_token');
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
});
adminHiringApi.interceptors.response.use(
    res => res,
    err => {
        if (err.response?.status === 401) {
            localStorage.removeItem('admin_hiring_token');
            localStorage.removeItem('admin_hiring_user');
        }
        return Promise.reject(err);
    }
);

// ── Worker Service ────────────────────────────────────────────────────────────
export const workerService = {
    register: (data) => axios.post(`${API_BASE_URL}/worker/register`, data),
    login: (data) => axios.post(`${API_BASE_URL}/worker/login`, data),
    getProfile: () => workerApi.get('/worker/profile'),
    getAvailableJobs: (params) => workerApi.get('/worker/available-jobs', { params }),
    applyJob: (data) => workerApi.post('/worker/apply-job', data),
    getApplicationStatus: () => workerApi.get('/worker/application-status'),
    getNotifications: (unreadOnly = false) => workerApi.get('/worker/notifications', { params: { unread_only: unreadOnly } }),
    markNotificationRead: (id) => workerApi.put(`/worker/notifications/${id}/read`),
    getReviews: () => workerApi.get('/worker/reviews'),
};

// ── Admin Hiring Service ──────────────────────────────────────────────────────
export const adminHiringService = {
    login: (credentials) => axios.post(`${API_BASE_URL}/admin/hiring/login`, credentials),
    createJob: (data) => adminHiringApi.post('/admin/hiring/create-job', data),
    getJobs: (statusFilter) => adminHiringApi.get('/admin/hiring/jobs', { params: { status_filter: statusFilter } }),
    getApplications: (params) => adminHiringApi.get('/admin/hiring/applications', { params }),
    updateApplicationStatus: (id, data) => adminHiringApi.put(`/admin/hiring/applications/${id}/status`, data),
    getAnalytics: () => adminHiringApi.get('/admin/hiring/analytics'),
    addWorkerReview: (aadhar, data) => adminHiringApi.post(`/admin/hiring/workers/${aadhar}/reviews`, data),
};

export default mainApi;
