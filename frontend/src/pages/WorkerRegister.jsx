import React, { useState } from 'react';
import {
    Container, Paper, Typography, TextField, Button, Grid,
    MenuItem, Alert, CircularProgress, Box, Stepper, Step,
    StepLabel, Snackbar, Link, Divider
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { workerService } from '../services/worker_service';
import WorkIcon from '@mui/icons-material/Work';

const steps = ['Personal Details', 'Professional Info', 'Account Security'];

const machineTypes = [
    'Weaving Machine', 'Spinning Machine', 'Knitting Machine', 'Dyeing Machine',
    'Cutting Machine', 'Sewing Machine', 'Embroidery Machine', 'Printing Machine'
];
const skillLevels = ['Beginner', 'Intermediate', 'Expert'];
const genders = ['Male', 'Female', 'Other'];

const WorkerRegister = () => {
    const navigate = useNavigate();
    const [activeStep, setActiveStep] = useState(0);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [snackbar, setSnackbar] = useState({ open: false, message: '' });

    const [formData, setFormData] = useState({
        aadhar_number: '', name: '', age: '', gender: '', phone: '',
        email: '', address: '', city: '', state: '',
        experience_years: '', previous_company: '', machine_type: '',
        skill_level: '', other_skills: '', expected_salary: '',
        password: '', confirmPassword: ''
    });

    const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

    const validateStep = () => {
        if (activeStep === 0) {
            if (!formData.aadhar_number || formData.aadhar_number.length !== 12 || !/^\d+$/.test(formData.aadhar_number))
                return 'Aadhar number must be exactly 12 digits.';
            if (!formData.name || !formData.age || !formData.gender || !formData.phone)
                return 'Please fill all required personal details.';
            if (!formData.address || !formData.city || !formData.state)
                return 'Please fill address details.';
        }
        if (activeStep === 1) {
            if (!formData.experience_years || !formData.machine_type || !formData.skill_level)
                return 'Please fill all professional details.';
        }
        if (activeStep === 2) {
            if (!formData.password || formData.password.length < 6)
                return 'Password must be at least 6 characters.';
            if (formData.password !== formData.confirmPassword)
                return 'Passwords do not match.';
        }
        return null;
    };

    const handleNext = () => {
        const err = validateStep();
        if (err) { setError(err); return; }
        setError('');
        setActiveStep(s => s + 1);
    };

    const handleBack = () => { setError(''); setActiveStep(s => s - 1); };

    const handleSubmit = async () => {
        const err = validateStep();
        if (err) { setError(err); return; }
        setLoading(true);
        try {
            const { confirmPassword, ...payload } = formData;
            await workerService.register(payload);
            setSnackbar({ open: true, message: 'Registration successful! Please login.' });
            setTimeout(() => navigate('/worker/login'), 2000);
        } catch (err) {
            setError(err.response?.data?.detail || 'Registration failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <Box sx={{
            minHeight: '100vh',
            background: 'linear-gradient(135deg, #1565C0 0%, #0D47A1 50%, #01579B 100%)',
            display: 'flex', alignItems: 'center', justifyContent: 'center', py: 4
        }}>
            <Container maxWidth="md">
                <Paper elevation={10} sx={{ p: 5, borderRadius: 4 }}>
                    <Box textAlign="center" mb={4}>
                        <Box sx={{
                            width: 64, height: 64, borderRadius: '50%',
                            background: 'linear-gradient(135deg, #1976d2, #42a5f5)',
                            display: 'flex', alignItems: 'center', justifyContent: 'center',
                            mx: 'auto', mb: 2
                        }}>
                            <WorkIcon sx={{ color: 'white', fontSize: 32 }} />
                        </Box>
                        <Typography variant="h5" fontWeight="bold" color="primary">Worker Registration</Typography>
                        <Typography variant="body2" color="text.secondary">Join the Antigravity Hiring Platform</Typography>
                    </Box>

                    <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
                        {steps.map(label => <Step key={label}><StepLabel>{label}</StepLabel></Step>)}
                    </Stepper>

                    {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

                    <Grid container spacing={3}>
                        {/* Step 0: Personal Details */}
                        {activeStep === 0 && <>
                            <Grid item xs={12} sm={6}>
                                <TextField fullWidth required label="Aadhar Number" name="aadhar_number"
                                    value={formData.aadhar_number} onChange={handleChange} inputProps={{ maxLength: 12 }}
                                    helperText="12-digit Aadhar number" />
                            </Grid>
                            <Grid item xs={12} sm={6}>
                                <TextField fullWidth required label="Full Name" name="name"
                                    value={formData.name} onChange={handleChange} />
                            </Grid>
                            <Grid item xs={12} sm={4}>
                                <TextField fullWidth required type="number" label="Age" name="age"
                                    value={formData.age} onChange={handleChange} inputProps={{ min: 18, max: 65 }} />
                            </Grid>
                            <Grid item xs={12} sm={4}>
                                <TextField fullWidth required select label="Gender" name="gender"
                                    value={formData.gender} onChange={handleChange}>
                                    {genders.map(g => <MenuItem key={g} value={g}>{g}</MenuItem>)}
                                </TextField>
                            </Grid>
                            <Grid item xs={12} sm={4}>
                                <TextField fullWidth required label="Phone" name="phone"
                                    value={formData.phone} onChange={handleChange} />
                            </Grid>
                            <Grid item xs={12}>
                                <TextField fullWidth required multiline rows={2} label="Address" name="address"
                                    value={formData.address} onChange={handleChange} />
                            </Grid>
                            <Grid item xs={12} sm={6}>
                                <TextField fullWidth required label="City" name="city"
                                    value={formData.city} onChange={handleChange} />
                            </Grid>
                            <Grid item xs={12} sm={6}>
                                <TextField fullWidth required label="State" name="state"
                                    value={formData.state} onChange={handleChange} />
                            </Grid>
                            <Grid item xs={12}>
                                <TextField fullWidth label="Email (optional)" name="email" type="email"
                                    value={formData.email} onChange={handleChange} />
                            </Grid>
                        </>}

                        {/* Step 1: Professional Info */}
                        {activeStep === 1 && <>
                            <Grid item xs={12} sm={6}>
                                <TextField fullWidth required type="number" label="Experience (Years)" name="experience_years"
                                    value={formData.experience_years} onChange={handleChange} inputProps={{ min: 0, max: 50, step: 0.5 }} />
                            </Grid>
                            <Grid item xs={12} sm={6}>
                                <TextField fullWidth label="Previous Company" name="previous_company"
                                    value={formData.previous_company} onChange={handleChange} />
                            </Grid>
                            <Grid item xs={12} sm={6}>
                                <TextField fullWidth required select label="Machine Type" name="machine_type"
                                    value={formData.machine_type} onChange={handleChange}>
                                    {machineTypes.map(m => <MenuItem key={m} value={m}>{m}</MenuItem>)}
                                </TextField>
                            </Grid>
                            <Grid item xs={12} sm={6}>
                                <TextField fullWidth required select label="Skill Level" name="skill_level"
                                    value={formData.skill_level} onChange={handleChange}>
                                    {skillLevels.map(s => <MenuItem key={s} value={s}>{s}</MenuItem>)}
                                </TextField>
                            </Grid>
                            <Grid item xs={12} sm={6}>
                                <TextField fullWidth type="number" label="Expected Salary (₹/month)" name="expected_salary"
                                    value={formData.expected_salary} onChange={handleChange} />
                            </Grid>
                            <Grid item xs={12} sm={6}>
                                <TextField fullWidth label="Other Skills" name="other_skills"
                                    value={formData.other_skills} onChange={handleChange}
                                    helperText="e.g. Quality check, maintenance" />
                            </Grid>
                        </>}

                        {/* Step 2: Account Security */}
                        {activeStep === 2 && <>
                            <Grid item xs={12}>
                                <Alert severity="info">Your Aadhar number <strong>{formData.aadhar_number}</strong> will be your login ID.</Alert>
                            </Grid>
                            <Grid item xs={12} sm={6}>
                                <TextField fullWidth required type="password" label="Password" name="password"
                                    value={formData.password} onChange={handleChange} helperText="Minimum 6 characters" />
                            </Grid>
                            <Grid item xs={12} sm={6}>
                                <TextField fullWidth required type="password" label="Confirm Password" name="confirmPassword"
                                    value={formData.confirmPassword} onChange={handleChange} />
                            </Grid>
                        </>}
                    </Grid>

                    <Box display="flex" justifyContent="space-between" mt={4}>
                        <Button onClick={handleBack} disabled={activeStep === 0} variant="outlined">Back</Button>
                        {activeStep < steps.length - 1
                            ? <Button onClick={handleNext} variant="contained">Next</Button>
                            : <Button onClick={handleSubmit} variant="contained" color="success" disabled={loading}>
                                {loading ? <CircularProgress size={22} color="inherit" /> : 'Register Now'}
                            </Button>
                        }
                    </Box>

                    <Divider sx={{ mt: 3, mb: 2 }} />
                    <Box textAlign="center">
                        <Typography variant="body2" color="text.secondary">
                            Already registered?{' '}
                            <Link onClick={() => navigate('/worker/login')} sx={{ cursor: 'pointer', fontWeight: 'bold' }}>
                                Login here
                            </Link>
                        </Typography>
                    </Box>
                </Paper>
            </Container>

            <Snackbar open={snackbar.open} autoHideDuration={3000}
                onClose={() => setSnackbar({ open: false, message: '' })}
                message={snackbar.message} />
        </Box>
    );
};

export default WorkerRegister;
