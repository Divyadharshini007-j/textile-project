import React, { useState } from 'react';
import {
    Container, Paper, Typography, TextField, Button,
    Box, Alert, CircularProgress, Link, Divider, Snackbar
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { workerService } from '../services/worker_service';
import { useAuth } from '../context/AuthContext';
import WorkIcon from '@mui/icons-material/Work';

const WorkerLogin = () => {
    const navigate = useNavigate();
    const { loginWorker } = useAuth();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [formData, setFormData] = useState({ aadhar_number: '', password: '' });

    const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        if (!formData.aadhar_number || !formData.password) {
            setError('Please enter your Aadhar number and password.');
            return;
        }
        setLoading(true);
        try {
            const response = await workerService.login(formData);
            const { access_token, user } = response.data;
            loginWorker(access_token, user);
            navigate('/worker/dashboard');
        } catch (err) {
            setError(err.response?.data?.detail || 'Login failed. Check your Aadhar number and password.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <Box sx={{
            minHeight: '100vh',
            background: 'linear-gradient(135deg, #1565C0 0%, #0D47A1 50%, #01579B 100%)',
            display: 'flex', alignItems: 'center', justifyContent: 'center'
        }}>
            <Container maxWidth="xs">
                <Paper elevation={10} sx={{ p: 5, borderRadius: 4 }}>
                    <Box textAlign="center" mb={3}>
                        <Box sx={{
                            width: 64, height: 64, borderRadius: '50%',
                            background: 'linear-gradient(135deg, #1976d2, #42a5f5)',
                            display: 'flex', alignItems: 'center', justifyContent: 'center',
                            mx: 'auto', mb: 2
                        }}>
                            <WorkIcon sx={{ color: 'white', fontSize: 32 }} />
                        </Box>
                        <Typography variant="h5" fontWeight="bold" color="primary">Worker Portal</Typography>
                        <Typography variant="body2" color="text.secondary" mt={0.5}>
                            Sign in with your Aadhar number
                        </Typography>
                    </Box>

                    {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

                    <Box component="form" onSubmit={handleSubmit}>
                        <TextField
                            fullWidth required label="Aadhar Number (12 digits)"
                            name="aadhar_number" value={formData.aadhar_number}
                            onChange={handleChange} margin="normal"
                            inputProps={{ maxLength: 12 }}
                            helperText="Enter your 12-digit Aadhar number"
                        />
                        <TextField
                            fullWidth required type="password" label="Password"
                            name="password" value={formData.password}
                            onChange={handleChange} margin="normal"
                        />
                        <Button
                            type="submit" fullWidth variant="contained" size="large"
                            disabled={loading}
                            sx={{ mt: 3, mb: 2, height: 50, borderRadius: 2, fontWeight: 'bold' }}
                        >
                            {loading ? <CircularProgress size={24} color="inherit" /> : 'Sign In'}
                        </Button>
                    </Box>

                    <Divider sx={{ my: 2 }} />
                    <Box textAlign="center">
                        <Typography variant="body2" color="text.secondary">
                            New worker?{' '}
                            <Link
                                onClick={() => navigate('/worker/register')}
                                sx={{ cursor: 'pointer', fontWeight: 'bold' }}
                            >
                                Register here
                            </Link>
                        </Typography>
                    </Box>
                </Paper>
            </Container>
        </Box>
    );
};

export default WorkerLogin;
