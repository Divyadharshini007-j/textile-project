import React, { useState, useEffect } from 'react';
import {
    Box, Typography, Paper, Table, TableBody, TableCell,
    TableContainer, TableHead, TableRow, Button, Dialog,
    DialogTitle, DialogContent, DialogActions, TextField,
    Stack, IconButton, Chip, Avatar, Alert, Select, MenuItem
} from '@mui/material';
import { Add as AddIcon, Business as SupplierIcon, Edit as EditIcon, Phone as PhoneIcon, Delete as DeleteIcon } from '@mui/icons-material';
import axios from 'axios';
import { useFormik } from 'formik';
import * as Yup from 'yup';

const API_BASE = 'https://textile-project.onrender.com/api';

const Suppliers = () => {
    const [suppliers, setSuppliers] = useState([]);
    const [open, setOpen] = useState(false);
    const [error, setError] = useState('');
    const [editingStatus, setEditingStatus] = useState(null);
    const fetchSuppliers = async () => {
        try {
            const res = await axios.get(`${API_BASE}/suppliers`);
            setSuppliers(res.data);
        } catch (err) {
            console.error(err);
        }
    };

    useEffect(() => {
        fetchSuppliers();
    }, []);

    const updateSupplierStatus = async (supplierId, newStatus) => {
        try {
            const supplier = suppliers.find(s => s.supplier_id === supplierId);
            if (!supplier) return;
            
            await axios.put(`${API_BASE}/suppliers/${supplierId}`, {
                ...supplier,
                status: newStatus
            });
            
            fetchSuppliers();
            setEditingStatus(null);
        } catch (err) {
            console.error('Failed to update supplier status:', err);
            setError('Failed to update supplier status');
        }
    };

    const deleteSupplier = async (supplierId) => {
        if (!window.confirm('Are you sure you want to delete this supplier?')) {
            return;
        }
        
        try {
            await axios.delete(`${API_BASE}/suppliers/${supplierId}`);
            fetchSuppliers();
        } catch (err) {
            console.error('Failed to delete supplier:', err);
            setError('Failed to delete supplier');
        }
    };

    const validationSchema = Yup.object({
        supplier_name: Yup.string().required('Supplier name is required').min(2, 'Name must be at least 2 characters').max(100, 'Name cannot exceed 100 characters'),
        contact_person: Yup.string().required('Contact person is required').min(2, 'Name must be at least 2 characters').max(50, 'Name cannot exceed 50 characters'),
        address: Yup.string().required('Address is required').min(10, 'Address must be at least 10 characters').max(200, 'Address cannot exceed 200 characters'),
        phone: Yup.string().matches(/^[6-9][0-9]{9}$/, 'Phone number must be a valid 10-digit number starting with 6-9').required('Phone is required'),
        email: Yup.string().email('Invalid email address').required('Email is required'),
        gstin: Yup.string().matches(/^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$/, 'Invalid GSTIN format (15 characters)').required('GSTIN is required'),
        payment_terms: Yup.string().required('Payment terms are required').oneOf(['NET 15', 'NET 30', 'NET 45', 'NET 60', 'ADVANCE'], 'Invalid payment terms')
    });

    const formik = useFormik({
        initialValues: {
            supplier_id: '',
            supplier_name: '',
            contact_person: '',
            address: '',
            phone: '',
            email: '',
            gstin: '',
            payment_terms: 'NET 30',
            opening_balance: 0
        },
        validationSchema: validationSchema,
        onSubmit: async (values, { resetForm }) => {
            try {
                // Generate supplier_id if not provided
                if (!values.supplier_id) {
                    values.supplier_id = 'SUPP' + Date.now().toString().slice(-6);
                }
                
                const submitData = { ...values };
                await axios.post(`${API_BASE}/suppliers/`, submitData);
                setOpen(false);
                setError('');
                fetchSuppliers();
                resetForm();
            } catch (err) {
                console.error(err);
                setError('Failed to save supplier');
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
                    <Typography variant="h4" sx={{ fontWeight: 700 }}>Suppliers</Typography>
                    <Typography variant="body2" color="textSecondary">Manage your raw material suppliers and procurement terms</Typography>
                </Box>
                <Button
                    variant="contained"
                    startIcon={<AddIcon />}
                    onClick={() => setOpen(true)}
                    sx={{ borderRadius: 2, px: 3, bgcolor: '#f44336', '&:hover': { bgcolor: '#d32f2f' } }}
                >
                    Add Supplier
                </Button>
            </Stack>

            <TableContainer component={Paper} sx={{ borderRadius: 3, boxShadow: '0 4px 20px rgba(0,0,0,0.05)' }}>
                <Table>
                    <TableHead sx={{ bgcolor: '#f8fafc' }}>
                        <TableRow>
                            <TableCell>Supplier</TableCell>
                            <TableCell>Contact</TableCell>
                            <TableCell>GSTIN</TableCell>
                            <TableCell>Terms</TableCell>
                            <TableCell align="right">Actions</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {suppliers.map((row) => (
                            <TableRow key={row.supplier_id} hover>
                                <TableCell>
                                    <Stack direction="row" spacing={2} alignItems="center">
                                        <Avatar sx={{ bgcolor: 'secondary.light' }}><SupplierIcon /></Avatar>
                                        <Box>
                                            <Typography variant="subtitle2">{row.supplier_name}</Typography>
                                            <Typography variant="caption" color="textSecondary">{row.supplier_id}</Typography>
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
                                <TableCell>{row.payment_terms}</TableCell>
                                <TableCell align="right">
                                    <IconButton
                                        size="small"
                                        onClick={() => deleteSupplier(row.supplier_id)}
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
                <DialogTitle>Add New Supplier</DialogTitle>
                <form onSubmit={formik.handleSubmit}>
                    <DialogContent dividers>
                        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
                        <Stack spacing={2} sx={{ mt: 1 }}>
                            <TextField name="supplier_id" label="Supplier ID" fullWidth value={formik.values.supplier_id} onChange={formik.handleChange} onBlur={formik.handleBlur} error={formik.touched.supplier_id && Boolean(formik.errors.supplier_id)} helperText={formik.touched.supplier_id && formik.errors.supplier_id} />
                            <TextField name="supplier_name" label="Supplier Name" fullWidth value={formik.values.supplier_name} onChange={formik.handleChange} onBlur={formik.handleBlur} error={formik.touched.supplier_name && Boolean(formik.errors.supplier_name)} helperText={formik.touched.supplier_name && formik.errors.supplier_name} />
                            <TextField name="contact_person" label="Contact Person" fullWidth value={formik.values.contact_person} onChange={formik.handleChange} onBlur={formik.handleBlur} error={formik.touched.contact_person && Boolean(formik.errors.contact_person)} helperText={formik.touched.contact_person && formik.errors.contact_person} />
                            <TextField name="phone" label="Phone" fullWidth value={formik.values.phone} onChange={formik.handleChange} onBlur={formik.handleBlur} error={formik.touched.phone && Boolean(formik.errors.phone)} helperText={formik.touched.phone && formik.errors.phone} />
                            <TextField name="email" label="Email" fullWidth value={formik.values.email} onChange={formik.handleChange} onBlur={formik.handleBlur} error={formik.touched.email && Boolean(formik.errors.email)} helperText={formik.touched.email && formik.errors.email} />
                            <TextField name="gstin" label="GSTIN" fullWidth value={formik.values.gstin} onChange={formik.handleChange} onBlur={formik.handleBlur} error={formik.touched.gstin && Boolean(formik.errors.gstin)} helperText={formik.touched.gstin && formik.errors.gstin} />
                            <TextField name="address" label="Address" fullWidth multiline rows={2} value={formik.values.address} onChange={formik.handleChange} onBlur={formik.handleBlur} error={formik.touched.address && Boolean(formik.errors.address)} helperText={formik.touched.address && formik.errors.address} />
                            <Stack direction="row" spacing={2}>
                                <TextField name="opening_balance" label="Opening Balance" type="number" fullWidth value={formik.values.opening_balance} onChange={formik.handleChange} onBlur={formik.handleBlur} error={formik.touched.opening_balance && Boolean(formik.errors.opening_balance)} helperText={formik.touched.opening_balance && formik.errors.opening_balance} />
                            </Stack>
                            <TextField name="payment_terms" label="Payment Terms" fullWidth value={formik.values.payment_terms} onChange={formik.handleChange} onBlur={formik.handleBlur} error={formik.touched.payment_terms && Boolean(formik.errors.payment_terms)} helperText={formik.touched.payment_terms && formik.errors.payment_terms} />
                        </Stack>
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={handleClose}>Cancel</Button>
                        <Button variant="contained" type="submit" color="error">Save Supplier</Button>
                    </DialogActions>
                </form>
            </Dialog>
        </Box>
    );
};

export default Suppliers;
