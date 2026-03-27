import React, { useState, useEffect } from 'react';
import {
    Container, Grid, Paper, Typography, Card, CardContent,
    Button, Box, Tabs, Tab, Table, TableBody, TableCell,
    TableContainer, TableHead, TableRow, Chip, Dialog,
    DialogTitle, DialogContent, DialogActions, TextField,
    MenuItem, CircularProgress, Snackbar, Alert, AppBar,
    Toolbar, IconButton, Tooltip, Divider
} from '@mui/material';
import {
    Add as AddIcon, BarChart as AnalyticsIcon,
    Assignment as AppIcon, Work as JobIcon,
    Logout as LogoutIcon, Refresh as RefreshIcon,
    AdminPanelSettings as AdminIcon
} from '@mui/icons-material';
import { adminHiringService } from '../services/worker_service';
import { useAuth } from '../context/AuthContext';
import {
    BarChart, Bar, XAxis, YAxis, CartesianGrid,
    Tooltip as RechartsTooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend
} from 'recharts';

const machineTypes = [
    'Weaving Machine', 'Spinning Machine', 'Knitting Machine', 'Dyeing Machine',
    'Cutting Machine', 'Sewing Machine', 'Embroidery Machine', 'Printing Machine'
];
const skillLevels = ['Beginner', 'Intermediate', 'Expert'];
const PIE_COLORS = ['#1976d2', '#2e7d32', '#ed6c02', '#9c27b0', '#d32f2f', '#0288d1', '#558b2f', '#f57c00'];

// ── Admin Login Gate ──────────────────────────────────────────────────────────
const AdminLoginGate = ({ onLogin }) => {
    const [creds, setCreds] = useState({ username: '', password: '' });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);
        try {
            const res = await adminHiringService.login(creds);
            onLogin(res.data.access_token, res.data.user);
        } catch (err) {
            setError(err.response?.data?.detail || 'Invalid credentials. Try hiring_admin / admin123');
        } finally {
            setLoading(false);
        }
    };

    return (
        <Box sx={{
            minHeight: '100vh',
            background: 'linear-gradient(135deg, #1a237e 0%, #283593 50%, #1565C0 100%)',
            display: 'flex', alignItems: 'center', justifyContent: 'center'
        }}>
            <Container maxWidth="xs">
                <Paper elevation={10} sx={{ p: 5, borderRadius: 4 }}>
                    <Box textAlign="center" mb={3}>
                        <Box sx={{
                            width: 64, height: 64, borderRadius: '50%',
                            background: 'linear-gradient(135deg, #1a237e, #3949ab)',
                            display: 'flex', alignItems: 'center', justifyContent: 'center',
                            mx: 'auto', mb: 2
                        }}>
                            <AdminIcon sx={{ color: 'white', fontSize: 32 }} />
                        </Box>
                        <Typography variant="h5" fontWeight="bold" color="primary">Admin Hiring Portal</Typography>
                        <Typography variant="body2" color="text.secondary" mt={0.5}>Sign in to manage hiring</Typography>
                    </Box>

                    {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

                    <Box component="form" onSubmit={handleSubmit}>
                        <TextField fullWidth required label="Username" value={creds.username}
                            onChange={e => setCreds({ ...creds, username: e.target.value })} margin="normal" />
                        <TextField fullWidth required type="password" label="Password" value={creds.password}
                            onChange={e => setCreds({ ...creds, password: e.target.value })} margin="normal" />
                        <Button type="submit" fullWidth variant="contained" size="large" disabled={loading}
                            sx={{ mt: 3, height: 50, borderRadius: 2, fontWeight: 'bold' }}>
                            {loading ? <CircularProgress size={24} color="inherit" /> : 'Sign In'}
                        </Button>
                    </Box>
                </Paper>
            </Container>
        </Box>
    );
};

// ── Main Admin Hiring Portal ──────────────────────────────────────────────────
const AdminHiring = () => {
    const { adminHiringUser, loginAdminHiring, logoutAdminHiring } = useAuth();
    const [activeTab, setActiveTab] = useState(0);
    const [jobs, setJobs] = useState([]);
    const [applications, setApplications] = useState([]);
    const [analytics, setAnalytics] = useState(null);
    const [loading, setLoading] = useState(false);
    const [jobDialogOpen, setJobDialogOpen] = useState(false);
    const [appDialogOpen, setAppDialogOpen] = useState(false);
    const [selectedApp, setSelectedApp] = useState(null);
    const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });

    const [jobForm, setJobForm] = useState({
        job_title: '', job_description: '', required_machine: '',
        required_experience: '', required_skill_level: 'Beginner',
        openings: 1, salary_min: '', salary_max: '',
        location: '', shift_type: 'Day', employment_type: 'Full_Time', closing_date: ''
    });

    const [appAction, setAppAction] = useState({
        status: 'Shortlisted', admin_notes: '', interview_date: '', offered_salary: ''
    });

    const [reviewForm, setReviewForm] = useState({ rating: 5, comments: '' });

    const isAuthenticated = !!(adminHiringUser || localStorage.getItem('admin_hiring_token'));

    // fetchData must be defined BEFORE useEffect
    const fetchData = async (tab = activeTab) => {
        setLoading(true);
        try {
            if (tab === 0) {
                const res = await adminHiringService.getJobs();
                setJobs(res.data);
            } else if (tab === 1) {
                const res = await adminHiringService.getApplications();
                setApplications(res.data);
            } else if (tab === 2) {
                const res = await adminHiringService.getAnalytics();
                setAnalytics(res.data);
            }
        } catch (err) {
            if (err.response?.status === 401) {
                logoutAdminHiring();
            } else {
                showSnackbar('Failed to load data.', 'error');
            }
        } finally {
            setLoading(false);
        }
    };

    const showSnackbar = (message, severity = 'success') => setSnackbar({ open: true, message, severity });

    useEffect(() => {
        if (isAuthenticated) fetchData(activeTab);
    }, [activeTab, isAuthenticated]);

    // Show login gate if not authenticated (after all hooks)
    if (!isAuthenticated) {
        return <AdminLoginGate onLogin={(token, user) => loginAdminHiring(token, user)} />;
    }

    const handleCreateJob = async () => {
        if (!jobForm.job_title || !jobForm.required_machine || !jobForm.location) {
            showSnackbar('Please fill all required fields.', 'error');
            return;
        }
        try {
            await adminHiringService.createJob(jobForm);
            setJobDialogOpen(false);
            setJobForm({
                job_title: '', job_description: '', required_machine: '',
                required_experience: '', required_skill_level: 'Beginner',
                openings: 1, salary_min: '', salary_max: '',
                location: '', shift_type: 'Day', employment_type: 'Full_Time', closing_date: ''
            });
            showSnackbar('Job posted successfully!');
            fetchData();
        } catch (err) {
            showSnackbar(err.response?.data?.detail || 'Failed to create job.', 'error');
        }
    };

    const handleAppAction = async () => {
        try {
            await adminHiringService.updateApplicationStatus(selectedApp.application_id, appAction);
            setAppDialogOpen(false);
            showSnackbar(`Application ${appAction.status.toLowerCase()} successfully!`);
            fetchData();
        } catch (err) {
            showSnackbar(err.response?.data?.detail || 'Failed to update application.', 'error');
        }
    };

    const handleSaveReview = async () => {
        try {
            await adminHiringService.addWorkerReview(selectedApp.aadhar_number, reviewForm);
            showSnackbar('Review saved successfully!');
            setReviewForm({ rating: 5, comments: '' });
        } catch (err) {
            showSnackbar(err.response?.data?.detail || 'Failed to save review.', 'error');
        }
    };

    const openReview = (app) => {
        setSelectedApp(app);
        setAppAction({ status: 'Shortlisted', admin_notes: '', interview_date: '', offered_salary: '' });
        setAppDialogOpen(true);
    };

    const statusColor = (s) => ({ Open: 'success', Closed: 'default', On_Hold: 'warning' }[s] || 'default');
    const appStatusColor = (s) => ({ Hired: 'success', Rejected: 'error', Shortlisted: 'info', Pending: 'warning' }[s] || 'default');

    return (
        <Box sx={{ minHeight: '100vh', bgcolor: '#f5f7fa' }}>
            {/* AppBar */}
            <AppBar position="static" elevation={0} sx={{ background: 'linear-gradient(90deg, #1a237e, #1565C0)' }}>
                <Toolbar>
                    <AdminIcon sx={{ mr: 1.5 }} />
                    <Typography variant="h6" fontWeight="bold" sx={{ flexGrow: 1 }}>
                        Admin Hiring Portal
                    </Typography>
                    <Typography variant="body2" sx={{ mr: 2, opacity: 0.85 }}>
                        {adminHiringUser?.username || localStorage.getItem('admin_hiring_user') ? JSON.parse(localStorage.getItem('admin_hiring_user') || '{}').username : ''}
                    </Typography>
                    <Tooltip title="Refresh">
                        <IconButton color="inherit" onClick={fetchData} size="small" sx={{ mr: 1 }}>
                            <RefreshIcon />
                        </IconButton>
                    </Tooltip>
                    <Button color="inherit" startIcon={<LogoutIcon />} onClick={logoutAdminHiring} size="small">
                        Logout
                    </Button>
                </Toolbar>
            </AppBar>

            <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
                {/* Stats Overview */}
                {analytics && (
                    <Grid container spacing={3} sx={{ mb: 4 }}>
                        {[
                            { label: 'Total Workers', val: analytics.overview.total_workers, color: '#e3f2fd' },
                            { label: 'Open Jobs', val: analytics.overview.open_jobs, color: '#e8f5e9' },
                            { label: 'Pending Applications', val: analytics.overview.pending_applications, color: '#fff3e0' },
                            { label: 'Total Hired', val: analytics.overview.hired_count, color: '#fce4ec' },
                        ].map((s, i) => (
                            <Grid item xs={6} sm={3} key={i}>
                                <Card elevation={2} sx={{ borderRadius: 3, bgcolor: s.color }}>
                                    <CardContent sx={{ textAlign: 'center', py: 2 }}>
                                        <Typography variant="h3" fontWeight="bold">{s.val}</Typography>
                                        <Typography variant="body2" color="text.secondary">{s.label}</Typography>
                                    </CardContent>
                                </Card>
                            </Grid>
                        ))}
                    </Grid>
                )}

                {/* Main Tabs */}
                <Paper elevation={3} sx={{ borderRadius: 3, overflow: 'hidden' }}>
                    <Tabs value={activeTab} onChange={(_, v) => setActiveTab(v)} variant="fullWidth"
                        sx={{ borderBottom: 1, borderColor: 'divider', bgcolor: 'white' }}>
                        <Tab label="Manage Jobs" icon={<JobIcon />} iconPosition="start" />
                        <Tab label="Review Applications" icon={<AppIcon />} iconPosition="start" />
                        <Tab label="Analytics" icon={<AnalyticsIcon />} iconPosition="start" />
                    </Tabs>

                    <Box sx={{ p: 3, minHeight: 500, bgcolor: '#fafafa' }}>
                        {loading && (
                            <Box display="flex" justifyContent="center" py={6}>
                                <CircularProgress />
                            </Box>
                        )}

                        {/* ── Jobs Tab ── */}
                        {!loading && activeTab === 0 && (
                            <Box>
                                <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                                    <Typography variant="h6" fontWeight="bold">Job Postings</Typography>
                                    <Button variant="contained" startIcon={<AddIcon />} onClick={() => setJobDialogOpen(true)}>
                                        Post New Job
                                    </Button>
                                </Box>
                                <TableContainer component={Paper} variant="outlined">
                                    <Table>
                                        <TableHead sx={{ bgcolor: '#e8eaf6' }}>
                                            <TableRow>
                                                <TableCell><strong>Job Title</strong></TableCell>
                                                <TableCell><strong>Machine</strong></TableCell>
                                                <TableCell><strong>Skill Level</strong></TableCell>
                                                <TableCell><strong>Exp</strong></TableCell>
                                                <TableCell><strong>Salary Range</strong></TableCell>
                                                <TableCell><strong>Location</strong></TableCell>
                                                <TableCell><strong>Openings</strong></TableCell>
                                                <TableCell><strong>Hired</strong></TableCell>
                                                <TableCell><strong>Status</strong></TableCell>
                                            </TableRow>
                                        </TableHead>
                                        <TableBody>
                                            {jobs.length === 0
                                                ? <TableRow><TableCell colSpan={9} align="center">No jobs posted yet.</TableCell></TableRow>
                                                : jobs.map(job => (
                                                    <TableRow key={job.job_id} hover>
                                                        <TableCell><strong>{job.job_title}</strong></TableCell>
                                                        <TableCell>{job.required_machine}</TableCell>
                                                        <TableCell>{job.required_skill_level}</TableCell>
                                                        <TableCell>{job.required_experience} yrs</TableCell>
                                                        <TableCell>
                                                            {job.salary_min ? `₹${job.salary_min?.toLocaleString()} – ${job.salary_max?.toLocaleString()}` : '—'}
                                                        </TableCell>
                                                        <TableCell>{job.location}</TableCell>
                                                        <TableCell>{job.openings}</TableCell>
                                                        <TableCell>{job.hired_count}</TableCell>
                                                        <TableCell><Chip label={job.status} color={statusColor(job.status)} size="small" /></TableCell>
                                                    </TableRow>
                                                ))
                                            }
                                        </TableBody>
                                    </Table>
                                </TableContainer>
                            </Box>
                        )}

                        {/* ── Applications Tab ── */}
                        {!loading && activeTab === 1 && (
                            <Box>
                                <Typography variant="h6" fontWeight="bold" mb={2}>Applications</Typography>
                                <TableContainer component={Paper} variant="outlined">
                                    <Table>
                                        <TableHead sx={{ bgcolor: '#e8eaf6' }}>
                                            <TableRow>
                                                <TableCell><strong>Worker Name</strong></TableCell>
                                                <TableCell><strong>Phone</strong></TableCell>
                                                <TableCell><strong>Job Title</strong></TableCell>
                                                <TableCell><strong>Machine</strong></TableCell>
                                                <TableCell><strong>Skill</strong></TableCell>
                                                <TableCell><strong>Exp</strong></TableCell>
                                                <TableCell><strong>Expected Salary</strong></TableCell>
                                                <TableCell><strong>Applied</strong></TableCell>
                                                <TableCell><strong>Status</strong></TableCell>
                                                <TableCell><strong>Action</strong></TableCell>
                                            </TableRow>
                                        </TableHead>
                                        <TableBody>
                                            {applications.length === 0
                                                ? <TableRow><TableCell colSpan={10} align="center">No applications yet.</TableCell></TableRow>
                                                : applications.map(app => (
                                                    <TableRow key={app.application_id} hover>
                                                        <TableCell><strong>{app.name}</strong></TableCell>
                                                        <TableCell>{app.phone}</TableCell>
                                                        <TableCell>{app.job_title}</TableCell>
                                                        <TableCell>{app.machine_type}</TableCell>
                                                        <TableCell>{app.skill_level}</TableCell>
                                                        <TableCell>{app.experience_years} yrs</TableCell>
                                                        <TableCell>{app.expected_salary ? `₹${app.expected_salary?.toLocaleString()}` : '—'}</TableCell>
                                                        <TableCell>{new Date(app.applied_date).toLocaleDateString('en-IN')}</TableCell>
                                                        <TableCell>
                                                            <Chip label={app.application_status} size="small" color={appStatusColor(app.application_status)} />
                                                        </TableCell>
                                                        <TableCell>
                                                            <Button size="small" variant="outlined" onClick={() => openReview(app)}>Review</Button>
                                                        </TableCell>
                                                    </TableRow>
                                                ))
                                            }
                                        </TableBody>
                                    </Table>
                                </TableContainer>
                            </Box>
                        )}

                        {/* ── Analytics Tab ── */}
                        {!loading && activeTab === 2 && analytics && (
                            <Grid container spacing={4}>
                                <Grid item xs={12} md={6}>
                                    <Typography variant="h6" fontWeight="bold" gutterBottom>Hiring Funnel</Typography>
                                    <Box height={300}>
                                        <ResponsiveContainer width="100%" height="100%">
                                            <BarChart data={[
                                                { name: 'Workers', count: analytics.overview.total_workers },
                                                { name: 'Available', count: analytics.overview.available_workers },
                                                { name: 'Applied', count: analytics.overview.total_applications },
                                                { name: 'Pending', count: analytics.overview.pending_applications },
                                                { name: 'Hired', count: analytics.overview.hired_count },
                                            ]}>
                                                <CartesianGrid strokeDasharray="3 3" />
                                                <XAxis dataKey="name" />
                                                <YAxis allowDecimals={false} />
                                                <RechartsTooltip />
                                                <Bar dataKey="count" fill="#1976d2" radius={[4, 4, 0, 0]} />
                                            </BarChart>
                                        </ResponsiveContainer>
                                    </Box>
                                </Grid>
                                <Grid item xs={12} md={6}>
                                    <Typography variant="h6" fontWeight="bold" gutterBottom>Workers by Machine Type</Typography>
                                    <Box height={300}>
                                        <ResponsiveContainer width="100%" height="100%">
                                            <PieChart>
                                                <Pie
                                                    data={analytics.workers_by_machine}
                                                    dataKey="count"
                                                    nameKey="machine_type"
                                                    cx="50%" cy="50%"
                                                    outerRadius={100}
                                                    label={({ machine_type, count }) => `${machine_type}: ${count}`}
                                                >
                                                    {analytics.workers_by_machine.map((_, i) => (
                                                        <Cell key={i} fill={PIE_COLORS[i % PIE_COLORS.length]} />
                                                    ))}
                                                </Pie>
                                                <RechartsTooltip />
                                                <Legend />
                                            </PieChart>
                                        </ResponsiveContainer>
                                    </Box>
                                </Grid>
                            </Grid>
                        )}
                    </Box>
                </Paper>
            </Container>

            {/* ── Post Job Dialog ── */}
            <Dialog open={jobDialogOpen} onClose={() => setJobDialogOpen(false)} fullWidth maxWidth="md">
                <DialogTitle>Post New Job</DialogTitle>
                <DialogContent sx={{ pt: 2 }}>
                    <Grid container spacing={2}>
                        <Grid item xs={12}>
                            <TextField fullWidth required label="Job Title" value={jobForm.job_title}
                                onChange={e => setJobForm({ ...jobForm, job_title: e.target.value })} />
                        </Grid>
                        <Grid item xs={12}>
                            <TextField fullWidth multiline rows={3} label="Job Description" value={jobForm.job_description}
                                onChange={e => setJobForm({ ...jobForm, job_description: e.target.value })} />
                        </Grid>
                        <Grid item xs={12} sm={6}>
                            <TextField select fullWidth required label="Required Machine" value={jobForm.required_machine}
                                onChange={e => setJobForm({ ...jobForm, required_machine: e.target.value })}>
                                {machineTypes.map(m => <MenuItem key={m} value={m}>{m}</MenuItem>)}
                            </TextField>
                        </Grid>
                        <Grid item xs={12} sm={6}>
                            <TextField select fullWidth required label="Required Skill Level" value={jobForm.required_skill_level}
                                onChange={e => setJobForm({ ...jobForm, required_skill_level: e.target.value })}>
                                {skillLevels.map(s => <MenuItem key={s} value={s}>{s}</MenuItem>)}
                            </TextField>
                        </Grid>
                        <Grid item xs={12} sm={4}>
                            <TextField fullWidth required type="number" label="Experience Required (Years)" value={jobForm.required_experience}
                                onChange={e => setJobForm({ ...jobForm, required_experience: e.target.value })} inputProps={{ min: 0, step: 0.5 }} />
                        </Grid>
                        <Grid item xs={12} sm={4}>
                            <TextField fullWidth required type="number" label="Number of Openings" value={jobForm.openings}
                                onChange={e => setJobForm({ ...jobForm, openings: e.target.value })} inputProps={{ min: 1 }} />
                        </Grid>
                        <Grid item xs={12} sm={4}>
                            <TextField fullWidth required label="Location" value={jobForm.location}
                                onChange={e => setJobForm({ ...jobForm, location: e.target.value })} />
                        </Grid>
                        <Grid item xs={12} sm={4}>
                            <TextField fullWidth type="number" label="Min Salary (₹/month)" value={jobForm.salary_min}
                                onChange={e => setJobForm({ ...jobForm, salary_min: e.target.value })} />
                        </Grid>
                        <Grid item xs={12} sm={4}>
                            <TextField fullWidth type="number" label="Max Salary (₹/month)" value={jobForm.salary_max}
                                onChange={e => setJobForm({ ...jobForm, salary_max: e.target.value })} />
                        </Grid>
                        <Grid item xs={12} sm={4}>
                            <TextField select fullWidth label="Shift Type" value={jobForm.shift_type}
                                onChange={e => setJobForm({ ...jobForm, shift_type: e.target.value })}>
                                {['Day', 'Night', 'Rotational'].map(s => <MenuItem key={s} value={s}>{s}</MenuItem>)}
                            </TextField>
                        </Grid>
                        <Grid item xs={12} sm={6}>
                            <TextField select fullWidth label="Employment Type" value={jobForm.employment_type}
                                onChange={e => setJobForm({ ...jobForm, employment_type: e.target.value })}>
                                {['Full_Time', 'Part_Time', 'Contract', 'Temporary'].map(t => (
                                    <MenuItem key={t} value={t}>{t.replace('_', ' ')}</MenuItem>
                                ))}
                            </TextField>
                        </Grid>
                        <Grid item xs={12} sm={6}>
                            <TextField fullWidth type="date" label="Closing Date" value={jobForm.closing_date}
                                onChange={e => setJobForm({ ...jobForm, closing_date: e.target.value })}
                                InputLabelProps={{ shrink: true }} />
                        </Grid>
                    </Grid>
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setJobDialogOpen(false)}>Cancel</Button>
                    <Button onClick={handleCreateJob} variant="contained">Post Job</Button>
                </DialogActions>
            </Dialog>

            {/* ── Review Application Dialog ── */}
            <Dialog open={appDialogOpen} onClose={() => setAppDialogOpen(false)} fullWidth maxWidth="sm">
                <DialogTitle>Review Application</DialogTitle>
                <DialogContent sx={{ pt: 2 }}>
                    {selectedApp && (
                        <Box sx={{ mb: 2, p: 2, bgcolor: '#f5f5f5', borderRadius: 2 }}>
                            <Typography variant="subtitle1" fontWeight="bold">{selectedApp.name}</Typography>
                            <Typography variant="body2">Job: {selectedApp.job_title}</Typography>
                            <Typography variant="body2">Machine: {selectedApp.machine_type} · {selectedApp.skill_level}</Typography>
                            <Typography variant="body2">Experience: {selectedApp.experience_years} years</Typography>
                            {selectedApp.expected_salary && (
                                <Typography variant="body2">Expected: ₹{selectedApp.expected_salary?.toLocaleString()}/month</Typography>
                            )}
                            {selectedApp.cover_letter && (
                                <Box mt={1}>
                                    <Typography variant="caption" color="text.secondary">Cover Letter:</Typography>
                                    <Typography variant="body2" sx={{ fontStyle: 'italic' }}>{selectedApp.cover_letter}</Typography>
                                </Box>
                            )}
                        </Box>
                    )}
                    <Grid container spacing={2}>
                        <Grid item xs={12}>
                            <TextField select fullWidth required label="Decision" value={appAction.status}
                                onChange={e => setAppAction({ ...appAction, status: e.target.value })}>
                                <MenuItem value="Shortlisted">✅ Shortlist for Interview</MenuItem>
                                <MenuItem value="Hired">🎉 Hire</MenuItem>
                                <MenuItem value="Rejected">❌ Reject</MenuItem>
                            </TextField>
                        </Grid>
                        <Grid item xs={12}>
                            <TextField fullWidth multiline rows={2} label="Notes to Worker (optional)" value={appAction.admin_notes}
                                onChange={e => setAppAction({ ...appAction, admin_notes: e.target.value })} />
                        </Grid>
                        {appAction.status === 'Shortlisted' && (
                            <Grid item xs={12}>
                                <TextField fullWidth type="datetime-local" label="Interview Date & Time"
                                    InputLabelProps={{ shrink: true }} value={appAction.interview_date}
                                    onChange={e => setAppAction({ ...appAction, interview_date: e.target.value })} />
                            </Grid>
                        )}
                        {appAction.status === 'Hired' && (
                            <Grid item xs={12}>
                                <TextField fullWidth type="number" label="Offered Salary (₹/month)" value={appAction.offered_salary}
                                    onChange={e => setAppAction({ ...appAction, offered_salary: e.target.value })} />
                            </Grid>
                        )}
                        <Grid item xs={12} sm={4}>
                            <TextField fullWidth type="number" label="Rating (1-5)" value={reviewForm.rating}
                                onChange={e => setReviewForm({ ...reviewForm, rating: Number(e.target.value) })} inputProps={{ min: 1, max: 5 }} />
                        </Grid>
                        <Grid item xs={12} sm={8}>
                            <TextField fullWidth label="Review comments" value={reviewForm.comments}
                                onChange={e => setReviewForm({ ...reviewForm, comments: e.target.value })} />
                        </Grid>
                    </Grid>
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setAppDialogOpen(false)}>Cancel</Button>
                    <Button onClick={handleSaveReview} variant="outlined">Save Review</Button>
                    <Button onClick={handleAppAction} variant="contained"
                        color={appAction.status === 'Rejected' ? 'error' : appAction.status === 'Hired' ? 'success' : 'primary'}>
                        Confirm {appAction.status}
                    </Button>
                </DialogActions>
            </Dialog>

            {/* Snackbar */}
            <Snackbar open={snackbar.open} autoHideDuration={4000}
                onClose={() => setSnackbar(s => ({ ...s, open: false }))}
                anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}>
                <Alert severity={snackbar.severity} onClose={() => setSnackbar(s => ({ ...s, open: false }))}>
                    {snackbar.message}
                </Alert>
            </Snackbar>
        </Box>
    );
};

export default AdminHiring;
