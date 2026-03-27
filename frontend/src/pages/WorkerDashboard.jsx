import React, { useState, useEffect } from 'react';
import {
    Container, Grid, Paper, Typography, Card, CardContent,
    Button, Badge, Box, Tabs, Tab, List, ListItem, ListItemText,
    Chip, IconButton, Dialog, DialogTitle, DialogContent, DialogActions,
    TextField, Snackbar, Alert, CircularProgress, Tooltip, Divider,
    AppBar, Toolbar
} from '@mui/material';
import {
    Work as WorkIcon, Assignment as AssignmentIcon,
    Notifications as NotificationsIcon, Person as PersonIcon,
    LocationOn as LocationIcon, AccessTime as TimeIcon,
    CheckCircle as CheckIcon, Logout as LogoutIcon,
    CurrencyRupee as RupeeIcon, Refresh as RefreshIcon
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { workerService } from '../services/worker_service';
import { useAuth } from '../context/AuthContext';

const statusColor = (s) => ({ Hired: 'success', Rejected: 'error', Shortlisted: 'info', Pending: 'warning' }[s] || 'default');

const WorkerDashboard = () => {
    const navigate = useNavigate();
    const { workerUser, logoutWorker } = useAuth();
    const [activeTab, setActiveTab] = useState(0);
    const [jobs, setJobs] = useState([]);
    const [applications, setApplications] = useState([]);
    const [notifications, setNotifications] = useState([]);
    const [allNotifications, setAllNotifications] = useState([]);
    const [reviews, setReviews] = useState([]);
    const [loading, setLoading] = useState(true);
    const [applyDialogOpen, setApplyDialogOpen] = useState(false);
    const [selectedJob, setSelectedJob] = useState(null);
    const [coverLetter, setCoverLetter] = useState('');
    const [applying, setApplying] = useState(false);
    const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });
    const [appliedJobIds, setAppliedJobIds] = useState(new Set());

    useEffect(() => {
        if (!localStorage.getItem('worker_token')) {
            navigate('/worker/login');
            return;
        }
        fetchData();
    }, []);

    useEffect(() => {
        if (!localStorage.getItem('worker_token')) return;
        fetchData();
    }, [activeTab]);

    useEffect(() => {
        const handler = () => {
            if (document.visibilityState === 'visible') fetchData();
        };
        document.addEventListener('visibilitychange', handler);
        return () => document.removeEventListener('visibilitychange', handler);
    }, []);

    useEffect(() => {
        const id = setInterval(() => {
            if (!localStorage.getItem('worker_token')) return;
            fetchData();
        }, 20000);
        return () => clearInterval(id);
    }, []);

    const fetchData = async () => {
        setLoading(true);
        try {
            const results = await Promise.allSettled([
                workerService.getAvailableJobs(),
                workerService.getApplicationStatus(),
                workerService.getNotifications(true),
                workerService.getNotifications(false),
                workerService.getReviews(),
            ]);

            const jobsRes = results[0].status === 'fulfilled' ? results[0].value : null;
            const appsRes = results[1].status === 'fulfilled' ? results[1].value : null;
            const notifsRes = results[2].status === 'fulfilled' ? results[2].value : null;
            const allNotifsRes = results[3].status === 'fulfilled' ? results[3].value : null;
            const reviewsRes = results[4].status === 'fulfilled' ? results[4].value : null;

            if (jobsRes) setJobs(jobsRes.data); else setJobs([]);
            if (appsRes) {
                setApplications(appsRes.data);
                setAppliedJobIds(new Set(appsRes.data.map(a => a.job_id)));
            } else {
                setApplications([]);
                setAppliedJobIds(new Set());
            }
            if (notifsRes) setNotifications(notifsRes.data); else setNotifications([]);
            if (allNotifsRes) setAllNotifications(allNotifsRes.data); else setAllNotifications([]);
            if (reviewsRes) setReviews(reviewsRes.data || []); else setReviews([]);

            const anyError = results.some(r => r.status === 'rejected' && r.reason?.response?.status !== 401);
            if (anyError) showSnackbar('Some data failed to load. Reviews are still shown.', 'error');
        } finally {
            setLoading(false);
        }
    };

    const showSnackbar = (message, severity = 'success') => setSnackbar({ open: true, message, severity });

    const handleApplyClick = (job) => { setSelectedJob(job); setApplyDialogOpen(true); };

    const handleApplySubmit = async () => {
        setApplying(true);
        try {
            await workerService.applyJob({ job_id: selectedJob.job_id, cover_letter: coverLetter });
            setApplyDialogOpen(false);
            setCoverLetter('');
            showSnackbar(`Successfully applied for ${selectedJob.job_title}!`);
            fetchData();
        } catch (err) {
            showSnackbar(err.response?.data?.detail || 'Failed to apply. You may have already applied.', 'error');
        } finally {
            setApplying(false);
        }
    };

    const markAsRead = async (id) => {
        try {
            await workerService.markNotificationRead(id);
            fetchData();
        } catch { }
    };

    const handleLogout = () => {
        logoutWorker();
        navigate('/worker/login');
    };

    const unreadCount = notifications.length;

    if (loading) {
        return (
            <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
                <CircularProgress size={60} />
            </Box>
        );
    }

    return (
        <Box sx={{ minHeight: '100vh', bgcolor: '#f5f7fa' }}>
            {/* Top AppBar */}
            <AppBar position="static" elevation={0} sx={{ background: 'linear-gradient(90deg, #1565C0, #0288D1)' }}>
                <Toolbar>
                    <WorkIcon sx={{ mr: 1.5 }} />
                    <Typography variant="h6" fontWeight="bold" sx={{ flexGrow: 1 }}>
                        Worker Portal
                    </Typography>
                    <Typography variant="body2" sx={{ mr: 2, opacity: 0.85 }}>
                        {workerUser?.name || 'Worker'}
                    </Typography>
                    <Tooltip title="Refresh">
                        <IconButton color="inherit" onClick={fetchData} size="small" sx={{ mr: 1 }}>
                            <RefreshIcon />
                        </IconButton>
                    </Tooltip>
                    <Button color="inherit" startIcon={<LogoutIcon />} onClick={handleLogout} size="small">
                        Logout
                    </Button>
                </Toolbar>
            </AppBar>

            <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
                {/* Profile Banner */}
                <Paper elevation={0} sx={{
                    p: 4, mb: 4, borderRadius: 4,
                    background: 'linear-gradient(135deg, #1976d2 0%, #42a5f5 100%)',
                    color: 'white'
                }}>
                    <Box display="flex" alignItems="center" gap={3}>
                        <Box sx={{
                            width: 72, height: 72, borderRadius: '50%',
                            bgcolor: 'rgba(255,255,255,0.2)',
                            display: 'flex', alignItems: 'center', justifyContent: 'center'
                        }}>
                            <PersonIcon sx={{ fontSize: 40 }} />
                        </Box>
                        <Box>
                            <Typography variant="h4" fontWeight="bold">
                                Hello, {workerUser?.name || 'Worker'}!
                            </Typography>
                            <Typography variant="subtitle1" sx={{ opacity: 0.9 }}>
                                {workerUser?.machine_type} · {workerUser?.skill_level} · {workerUser?.availability_status || 'Available'}
                            </Typography>
                        </Box>
                    </Box>
                </Paper>

                {/* Stats Cards */}
                <Grid container spacing={3} sx={{ mb: 4 }}>
                    {[
                        { label: 'Available Jobs', val: jobs.length, icon: <WorkIcon sx={{ fontSize: 36, color: '#1976d2' }} />, color: '#e3f2fd' },
                        { label: 'My Applications', val: applications.length, icon: <AssignmentIcon sx={{ fontSize: 36, color: '#2e7d32' }} />, color: '#e8f5e9' },
                        { label: 'Unread Notifications', val: unreadCount, icon: <NotificationsIcon sx={{ fontSize: 36, color: '#c62828' }} />, color: '#ffebee' },
                    ].map((s, i) => (
                        <Grid item xs={12} sm={4} key={i}>
                            <Card elevation={2} sx={{ borderRadius: 3, bgcolor: s.color, border: 'none' }}>
                                <CardContent sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', p: 3 }}>
                                    <Box>
                                        <Typography variant="h3" fontWeight="bold">{s.val}</Typography>
                                        <Typography variant="body2" color="text.secondary" mt={0.5}>{s.label}</Typography>
                                    </Box>
                                    {s.icon}
                                </CardContent>
                            </Card>
                        </Grid>
                    ))}
                </Grid>

                {/* Main Tabs */}
                <Paper elevation={3} sx={{ borderRadius: 3, overflow: 'hidden' }}>
                    <Tabs
                        value={activeTab} onChange={(_, v) => setActiveTab(v)}
                        variant="fullWidth"
                        sx={{ borderBottom: 1, borderColor: 'divider', bgcolor: 'white' }}
                    >
                        <Tab label="Find Jobs" icon={<WorkIcon />} iconPosition="start" />
                        <Tab label="My Applications" icon={<AssignmentIcon />} iconPosition="start" />
                        <Tab
                            label="Notifications"
                            icon={
                                <Badge badgeContent={unreadCount} color="error">
                                    <NotificationsIcon />
                                </Badge>
                            }
                            iconPosition="start"
                        />
                        <Tab label="Reviews" icon={<AssignmentIcon />} iconPosition="start" />
                    </Tabs>

                    <Box sx={{ p: 3, minHeight: 400, bgcolor: '#fafafa' }}>
                        {/* ── Find Jobs ── */}
                        {activeTab === 0 && (
                            <Grid container spacing={2}>
                                {jobs.length === 0
                                    ? <Grid item xs={12}><Alert severity="info">No jobs matching your skills right now. Check back later.</Alert></Grid>
                                    : jobs.map(job => (
                                        <Grid item xs={12} key={job.job_id}>
                                            <Card variant="outlined" sx={{ borderRadius: 2, '&:hover': { boxShadow: 4 }, transition: 'box-shadow 0.2s' }}>
                                                <CardContent>
                                                    <Box display="flex" justifyContent="space-between" alignItems="flex-start" flexWrap="wrap" gap={2}>
                                                        <Box flex={1}>
                                                            <Box display="flex" alignItems="center" gap={1} mb={0.5}>
                                                                <Typography variant="h6" color="primary" fontWeight="bold">{job.job_title}</Typography>
                                                                <Chip label={job.employment_type?.replace('_', ' ')} size="small" variant="outlined" />
                                                            </Box>
                                                            <Box display="flex" gap={2} flexWrap="wrap" mb={1}>
                                                                <Box display="flex" alignItems="center" gap={0.5} color="text.secondary">
                                                                    <LocationIcon fontSize="small" />
                                                                    <Typography variant="caption">{job.location}</Typography>
                                                                </Box>
                                                                <Box display="flex" alignItems="center" gap={0.5} color="text.secondary">
                                                                    <TimeIcon fontSize="small" />
                                                                    <Typography variant="caption">{job.shift_type} Shift</Typography>
                                                                </Box>
                                                                <Box display="flex" alignItems="center" gap={0.5} color="text.secondary">
                                                                    <WorkIcon fontSize="small" />
                                                                    <Typography variant="caption">{job.required_experience}+ yrs · {job.required_skill_level}</Typography>
                                                                </Box>
                                                            </Box>
                                                            <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                                                                {job.job_description}
                                                            </Typography>
                                                            <Typography variant="caption" color="text.disabled">
                                                                {job.openings - job.hired_count} opening(s) remaining
                                                            </Typography>
                                                        </Box>
                                                        <Box textAlign="right" minWidth={140}>
                                                            {job.salary_min && (
                                                                <Typography variant="h6" color="success.main" fontWeight="bold">
                                                                    ₹{job.salary_min.toLocaleString()} – {job.salary_max?.toLocaleString()}
                                                                </Typography>
                                                            )}
                                                            <Typography variant="caption" color="text.secondary" display="block" mb={1}>per month</Typography>
                                                            {appliedJobIds.has(job.job_id)
                                                                ? <Chip label="Applied" color="success" icon={<CheckIcon />} />
                                                                : <Button variant="contained" onClick={() => handleApplyClick(job)} sx={{ borderRadius: 2 }}>
                                                                    Apply Now
                                                                </Button>
                                                            }
                                                        </Box>
                                                    </Box>
                                                </CardContent>
                                            </Card>
                                        </Grid>
                                    ))
                                }
                            </Grid>
                        )}

                        {/* ── My Applications ── */}
                        {activeTab === 1 && (
                            <List disablePadding>
                                {applications.length === 0
                                    ? <Alert severity="info">You haven't applied to any jobs yet. Browse available jobs!</Alert>
                                    : applications.map(app => (
                                        <Paper key={app.application_id} variant="outlined" sx={{ mb: 2, borderRadius: 2 }}>
                                            <ListItem sx={{ py: 2, flexWrap: 'wrap', gap: 1 }}>
                                                <ListItemText
                                                    primary={<Typography variant="h6" fontWeight="bold">{app.job_title}</Typography>}
                                                    secondary={
                                                        <Box>
                                                            <Typography variant="body2" color="text.secondary">
                                                                Applied: {new Date(app.applied_date).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })}
                                                            </Typography>
                                                            {app.admin_notes && (
                                                                <Typography variant="body2" sx={{ mt: 0.5, fontStyle: 'italic', color: 'text.secondary' }}>
                                                                    Note: {app.admin_notes}
                                                                </Typography>
                                                            )}
                                                            {app.interview_date && (
                                                                <Alert severity="info" sx={{ mt: 1, py: 0 }}>
                                                                    Interview scheduled: {new Date(app.interview_date).toLocaleString('en-IN')}
                                                                </Alert>
                                                            )}
                                                        </Box>
                                                    }
                                                />
                                                <Chip
                                                    label={app.application_status}
                                                    color={statusColor(app.application_status)}
                                                    sx={{ fontWeight: 'bold', minWidth: 100 }}
                                                />
                                            </ListItem>
                                        </Paper>
                                    ))
                                }
                            </List>
                        )}

                        {/* ── Notifications ── */}
                        {activeTab === 2 && (
                            <List disablePadding>
                                {allNotifications.length === 0
                                    ? <Alert severity="info">No notifications yet.</Alert>
                                    : allNotifications.map(n => (
                                        <Paper
                                            key={n.notification_id}
                                            variant="outlined"
                                            sx={{
                                                mb: 1.5, borderRadius: 2,
                                                bgcolor: n.is_read ? 'white' : '#e8f4fd',
                                                borderColor: n.is_read ? 'divider' : '#1976d2'
                                            }}
                                        >
                                            <ListItem
                                                secondaryAction={
                                                    !n.is_read && (
                                                        <Tooltip title="Mark as read">
                                                            <IconButton onClick={() => markAsRead(n.notification_id)} color="primary">
                                                                <CheckIcon />
                                                            </IconButton>
                                                        </Tooltip>
                                                    )
                                                }
                                            >
                                                <ListItemText
                                                    primary={
                                                        <Box display="flex" alignItems="center" gap={1}>
                                                            <Typography fontWeight={n.is_read ? 'normal' : 'bold'}>{n.title}</Typography>
                                                            {!n.is_read && <Chip label="New" size="small" color="primary" />}
                                                        </Box>
                                                    }
                                                    secondary={
                                                        <Box>
                                                            <Typography variant="body2">{n.message}</Typography>
                                                            <Typography variant="caption" color="text.disabled">
                                                                {new Date(n.created_at).toLocaleString('en-IN')}
                                                            </Typography>
                                                        </Box>
                                                    }
                                                />
                                            </ListItem>
                                        </Paper>
                                    ))
                                }
                            </List>
                        )}

                        {activeTab === 3 && (
                            <List disablePadding>
                                {reviews.length === 0
                                    ? <Alert severity="info">No reviews yet.</Alert>
                                    : reviews.map(r => (
                                        <Paper key={r.review_id} variant="outlined" sx={{ mb: 1.5, borderRadius: 2 }}>
                                            <ListItem>
                                                <ListItemText
                                                    primary={<Typography variant="h6">Rating: {r.rating}/5</Typography>}
                                                    secondary={
                                                        <Box>
                                                            <Typography variant="body2">{r.comments || 'No comments provided'}</Typography>
                                                            <Typography variant="caption" color="text.disabled">
                                                                {new Date(r.created_at).toLocaleString('en-IN')}
                                                            </Typography>
                                                        </Box>
                                                    }
                                                />
                                            </ListItem>
                                        </Paper>
                                    ))
                                }
                            </List>
                        )}
                    </Box>
                </Paper>
            </Container>

            {/* Apply Dialog */}
            <Dialog open={applyDialogOpen} onClose={() => setApplyDialogOpen(false)} fullWidth maxWidth="sm">
                <DialogTitle>Apply for: {selectedJob?.job_title}</DialogTitle>
                <DialogContent>
                    <Box sx={{ mb: 2 }}>
                        <Typography variant="body2" color="text.secondary" gutterBottom>
                            <strong>Location:</strong> {selectedJob?.location} &nbsp;|&nbsp;
                            <strong>Salary:</strong> ₹{selectedJob?.salary_min?.toLocaleString()} – {selectedJob?.salary_max?.toLocaleString()}
                        </Typography>
                    </Box>
                    <TextField
                        fullWidth multiline rows={4}
                        label="Cover Letter / Why should we hire you?"
                        value={coverLetter}
                        onChange={(e) => setCoverLetter(e.target.value)}
                        placeholder="Describe your relevant experience and why you're a great fit..."
                    />
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setApplyDialogOpen(false)}>Cancel</Button>
                    <Button onClick={handleApplySubmit} variant="contained" disabled={applying}>
                        {applying ? <CircularProgress size={20} /> : 'Submit Application'}
                    </Button>
                </DialogActions>
            </Dialog>

            {/* Snackbar */}
            <Snackbar
                open={snackbar.open}
                autoHideDuration={4000}
                onClose={() => setSnackbar(s => ({ ...s, open: false }))}
                anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
            >
                <Alert severity={snackbar.severity} onClose={() => setSnackbar(s => ({ ...s, open: false }))}>
                    {snackbar.message}
                </Alert>
            </Snackbar>
        </Box>
    );
};

export default WorkerDashboard;
