import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [mainUser, setMainUser] = useState(null);
    const [workerUser, setWorkerUser] = useState(null);
    const [adminHiringUser, setAdminHiringUser] = useState(null);

    useEffect(() => {
        // Load persisted sessions on mount
        const mainToken = localStorage.getItem('token');
        const workerToken = localStorage.getItem('worker_token');
        const adminToken = localStorage.getItem('admin_hiring_token');

        if (mainToken) {
            try { setMainUser(JSON.parse(localStorage.getItem('main_user') || 'null')); } catch { }
        }
        if (workerToken) {
            try { setWorkerUser(JSON.parse(localStorage.getItem('worker_user') || 'null')); } catch { }
        }
        if (adminToken) {
            try { setAdminHiringUser(JSON.parse(localStorage.getItem('admin_hiring_user') || 'null')); } catch { }
        }
    }, []);

    const loginWorker = (token, user) => {
        localStorage.setItem('worker_token', token);
        localStorage.setItem('worker_user', JSON.stringify(user));
        setWorkerUser(user);
    };

    const logoutWorker = () => {
        localStorage.removeItem('worker_token');
        localStorage.removeItem('worker_user');
        setWorkerUser(null);
    };

    const loginAdminHiring = (token, user) => {
        localStorage.setItem('admin_hiring_token', token);
        localStorage.setItem('admin_hiring_user', JSON.stringify(user));
        setAdminHiringUser(user);
    };

    const logoutAdminHiring = () => {
        localStorage.removeItem('admin_hiring_token');
        localStorage.removeItem('admin_hiring_user');
        setAdminHiringUser(null);
    };

    const loginMain = (token, user) => {
        localStorage.setItem('token', token);
        localStorage.setItem('main_user', JSON.stringify(user));
        setMainUser(user);
    };

    const logoutMain = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('main_user');
        setMainUser(null);
    };

    return (
        <AuthContext.Provider value={{
            mainUser, workerUser, adminHiringUser,
            loginWorker, logoutWorker,
            loginAdminHiring, logoutAdminHiring,
            loginMain, logoutMain,
        }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const ctx = useContext(AuthContext);
    if (!ctx) throw new Error('useAuth must be used within AuthProvider');
    return ctx;
};

export default AuthContext;
