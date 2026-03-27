import React, { useState, useEffect } from 'react';
import {
    Box, Typography, Paper, Table, TableBody, TableCell,
    TableContainer, TableHead, TableRow, Button, Dialog,
    DialogTitle, DialogContent, DialogActions, TextField,
    Stack, IconButton, Chip, Avatar, Alert, Select, MenuItem
} from '@mui/material';
import { Add as AddIcon, Person as CustomerIcon, Edit as EditIcon, Phone as PhoneIcon, Delete as DeleteIcon } from '@mui/icons-material';
import axios from 'axios';
import { useFormik } from 'formik';
import * as Yup from 'yup';

const API_BASE = 'http://localhost:8000/api';

const Customers = () => {
    const [customers, setCustomers] = useState([]);
    const [open, setOpen] = useState(false);
    const [error, setError] = useState('');
    const [editingStatus, setEditingStatus] = useState(null);
    const fetchCustomers = async () => {
        try {
            const res = await axios.get(`${API_BASE}/customers`);
            setCustomers(res.data);
        } catch (err) {
            console.error(err);
        }
    };

    useEffect(() => {
        fetchCustomers();
    }, []);

    const updateCustomerStatus = async (customerId, newStatus) => {
        try {
            const customer = customers.find(c => c.customer_id === customerId);
            if (!customer) return;
            
            await axios.put(`${API_BASE}/customers/${customerId}`, {
                ...customer,
                status: newStatus
            });
            
            fetchCustomers();
            setEditingStatus(null);
        } catch (err) {
            console.error('Failed to update customer status:', err);
            setError('Failed to update customer status');
        }
    };

    const deleteCustomer = async (customerId) => {
        if (!window.confirm('Are you sure you want to delete this customer?')) {
            return;
        }
        
        try {
            await axios.delete(`${API_BASE}/customers/${customerId}`);
            fetchCustomers();
        } catch (err) {
            console.error('Failed to delete customer:', err);
            setError('Failed to delete customer');
        }
    };

    const validationSchema = Yup.object({
        customer_name: Yup.string().required('Customer name is required').min(2, 'Name must be at least 2 characters').max(100, 'Name cannot exceed 100 characters'),
        contact_person: Yup.string().required('Contact person is required').min(2, 'Name must be at least 2 characters').max(50, 'Name cannot exceed 50 characters'),
        address: Yup.string().required('Address is required').min(10, 'Address must be at least 10 characters').max(200, 'Address cannot exceed 200 characters'),
        city: Yup.string().required('City is required').min(2, 'City must be at least 2 characters').max(50, 'City cannot exceed 50 characters'),
        country: Yup.string().required('Country is required').min(2, 'Country must be at least 2 characters').max(50, 'Country cannot exceed 50 characters'),
        phone: Yup.string().matches(/^[6-9][0-9]{9}$/, 'Phone number must be a valid 10-digit number starting with 6-9').required('Phone is required'),
        email: Yup.string().email('Invalid email address').required('Email is required'),
        gstin: Yup.string().matches(/^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$/, 'Invalid GSTIN format (15 characters)').required('GSTIN is required'),
        credit_limit: Yup.number().typeError('Must be a number').min(0, 'Credit limit cannot be negative').max(1000000, 'Credit limit cannot exceed 10,00,000'),
        payment_terms: Yup.string().required('Payment terms are required').oneOf(['NET 15', 'NET 30', 'NET 45', 'NET 60', 'ADVANCE'], 'Invalid payment terms')
    });

    const formik = useFormik({
        initialValues: {
            customer_id: '',
            customer_name: '',
            contact_person: '',
            address: '',
            city: '',
            country: 'India',
            phone: '',
            email: '',
            gstin: '',
            credit_limit: 0,
            opening_balance: 0,
            payment_terms: 'NET 30'
        },
        validationSchema: validationSchema,
        onSubmit: async (values, { resetForm }) => {
            try {
                // Generate customer_id if not provided
                if (!values.customer_id) {
                    values.customer_id = 'CUST' + Date.now().toString().slice(-6);
                }
                
                const submitData = { ...values };
                await axios.post(`${API_BASE}/customers/`, submitData);
                setOpen(false);
                setError('');
                fetchCustomers();
                resetForm();
            } catch (err) {
                console.error(err);
                setError('Failed to save customer');
            }
        },
    });

    const handleClose = () => {
        setOpen(false);
        formik.resetForm();
        setError('');
    };

    return (
        <Box sx={{ flexGrow: 1 }}>
            <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 4 }}>
                <Box>
                    <Typography variant="h4" sx={{ fontWeight: 700 }}>Customers</Typography>
                    <Typography variant="body2" color="textSecondary">Manage your customer base and credit limits</Typography>
                </Box>
                <Button
                    variant="contained"
                    startIcon={<AddIcon />}
                    onClick={() => setOpen(true)}
                    sx={{ borderRadius: 2, px: 3 }}
                >
                    Add Customer
                </Button>
            </Stack>

            <TableContainer component={Paper} sx={{ borderRadius: 3, boxShadow: '0 4px 20px rgba(0,0,0,0.05)' }}>
                <Table>
                    <TableHead sx={{ bgcolor: '#f8fafc' }}>
                        <TableRow>
                            <TableCell>Customer</TableCell>
                            <TableCell>Contact</TableCell>
                            <TableCell>GSTIN</TableCell>
                            <TableCell>City</TableCell>
                            <TableCell align="right">Actions</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {customers.map((row) => (
                            <TableRow key={row.customer_id} hover>
                                <TableCell>
                                    <Stack direction="row" spacing={2} alignItems="center">
                                        <Avatar sx={{ bgcolor: 'primary.light' }}><CustomerIcon /></Avatar>
                                        <Box>
                                            <Typography variant="subtitle2">{row.customer_name}</Typography>
                                            <Typography variant="caption" color="textSecondary">{row.customer_id}</Typography>
                                        </Box>
                                    </Stack>
                                </TableCell>
                                <TableCell>
                                    <Box>
                                        <Typography variant="body2">{row.contact_person}</Typography>
                                        <Typography variant="caption" color="textSecondary">{row.phone}</Typography>
                                    </Box>
                                </TableCell>
                                <TableCell>{row.gstin}</TableCell>
                                <TableCell>{row.city}</TableCell>
                                <TableCell align="right">
                                    <IconButton
                                        size="small"
                                        onClick={() => deleteCustomer(row.customer_id)}
                                        color="error"
                                        sx={{ p: 0.5 }}
                                    >
                                        <DeleteIcon fontSize="small" />
                                    </IconButton>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>

            <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
                <DialogTitle>Add New Customer</DialogTitle>
                <form onSubmit={formik.handleSubmit}>
                    <DialogContent dividers>
                        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
                        <Stack spacing={2} sx={{ mt: 1 }}>
                            <TextField name="customer_id" label="Customer ID" fullWidth value={formik.values.customer_id} onChange={formik.handleChange} onBlur={formik.handleBlur} error={formik.touched.customer_id && Boolean(formik.errors.customer_id)} helperText={formik.touched.customer_id && formik.errors.customer_id} />
                            <TextField name="customer_name" label="Customer Name" fullWidth value={formik.values.customer_name} onChange={formik.handleChange} onBlur={formik.handleBlur} error={formik.touched.customer_name && Boolean(formik.errors.customer_name)} helperText={formik.touched.customer_name && formik.errors.customer_name} />
                            <TextField name="contact_person" label="Contact Person" fullWidth value={formik.values.contact_person} onChange={formik.handleChange} onBlur={formik.handleBlur} error={formik.touched.contact_person && Boolean(formik.errors.contact_person)} helperText={formik.touched.contact_person && formik.errors.contact_person} />
                            <TextField name="phone" label="Phone" fullWidth value={formik.values.phone} onChange={formik.handleChange} onBlur={formik.handleBlur} error={formik.touched.phone && Boolean(formik.errors.phone)} helperText={formik.touched.phone && formik.errors.phone} />
                            <TextField name="email" label="Email" fullWidth value={formik.values.email} onChange={formik.handleChange} onBlur={formik.handleBlur} error={formik.touched.email && Boolean(formik.errors.email)} helperText={formik.touched.email && formik.errors.email} />
                            <TextField name="gstin" label="GSTIN" fullWidth value={formik.values.gstin} onChange={formik.handleChange} onBlur={formik.handleBlur} error={formik.touched.gstin && Boolean(formik.errors.gstin)} helperText={formik.touched.gstin && formik.errors.gstin} />
                            <TextField name="address" label="Address" fullWidth multiline rows={2} value={formik.values.address} onChange={formik.handleChange} onBlur={formik.handleBlur} error={formik.touched.address && Boolean(formik.errors.address)} helperText={formik.touched.address && formik.errors.address} />
                            <Stack direction="row" spacing={2}>
                                <TextField name="city" label="City" fullWidth value={formik.values.city} onChange={formik.handleChange} onBlur={formik.handleBlur} error={formik.touched.city && Boolean(formik.errors.city)} helperText={formik.touched.city && formik.errors.city} />
                                <TextField name="country" label="Country" fullWidth value={formik.values.country} onChange={formik.handleChange} onBlur={formik.handleBlur} error={formik.touched.country && Boolean(formik.errors.country)} helperText={formik.touched.country && formik.errors.country} />
                            </Stack>
                            <Stack direction="row" spacing={2}>
                                <TextField name="credit_limit" label="Credit Limit" type="number" fullWidth value={formik.values.credit_limit} onChange={formik.handleChange} onBlur={formik.handleBlur} error={formik.touched.credit_limit && Boolean(formik.errors.credit_limit)} helperText={formik.touched.credit_limit && formik.errors.credit_limit} />
                                <TextField name="opening_balance" label="Opening Balance" type="number" fullWidth value={formik.values.opening_balance} onChange={formik.handleChange} onBlur={formik.handleBlur} error={formik.touched.opening_balance && Boolean(formik.errors.opening_balance)} helperText={formik.touched.opening_balance && formik.errors.opening_balance} />
                            </Stack>
                            <TextField
                                name="payment_terms"
                                label="Payment Terms"
                                select
                                fullWidth
                                value={formik.values.payment_terms}
                                onChange={formik.handleChange}
                                onBlur={formik.handleBlur}
                                error={formik.touched.payment_terms && Boolean(formik.errors.payment_terms)}
                                helperText={formik.touched.payment_terms && formik.errors.payment_terms}
                            >
                                <MenuItem value="NET 15">NET 15</MenuItem>
                                <MenuItem value="NET 30">NET 30</MenuItem>
                                <MenuItem value="NET 45">NET 45</MenuItem>
                                <MenuItem value="NET 60">NET 60</MenuItem>
                                <MenuItem value="ADVANCE">ADVANCE</MenuItem>
                            </TextField>
                        </Stack>
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={handleClose}>Cancel</Button>
                        <Button variant="contained" type="submit">Save Customer</Button>
                    </DialogActions>
                </form>
            </Dialog>
        </Box>
    );
};

export default Customers;
