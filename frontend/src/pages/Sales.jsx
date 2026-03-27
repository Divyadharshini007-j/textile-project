import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
    Box, Typography, TextField, Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow,
    Paper, Dialog, DialogTitle, DialogContent, DialogActions, Stack, Alert, IconButton, Chip, Select, MenuItem,
    InputAdornment
} from '@mui/material';
import { Add as AddIcon, Edit as EditIcon, Receipt as ReceiptIcon, Delete as DeleteIcon } from '@mui/icons-material';
import { useFormik } from 'formik';
import * as Yup from 'yup';

const API_BASE = 'http://localhost:8000/api';

const Sales = () => {
    const [sales, setSales] = useState([]);
    const [productTypes, setProductTypes] = useState([]);
    const [open, setOpen] = useState(false);
    const [error, setError] = useState('');
    const [editingPayment, setEditingPayment] = useState(null); // Track which row is being edited
    const [editingStatus, setEditingStatus] = useState(null); // Track which row is being edited for status

    const fetchData = async () => {
        try {
            const [salesRes, productTypesRes] = await Promise.all([
                axios.get(`${API_BASE}/sales/`),
                axios.get(`${API_BASE}/predictions/yarn-types`) // Fixed endpoint
            ]);
            setSales(salesRes.data);
            setProductTypes(productTypesRes.data); // Set product types
        } catch (err) {
            console.error('Failed to fetch data:', err);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    const updatePaymentStatus = async (saleId, newStatus) => {
        try {
            // Find the sale record
            const sale = sales.find(s => s.sales_id === saleId);
            if (!sale) return;

            // Update the sale with new payment status
            await axios.put(`${API_BASE}/sales/${saleId}`, {
                ...sale,
                payment_status: newStatus
            });

            // Refresh data
            fetchData();
            setEditingStatus(null); // Exit edit mode
        } catch (err) {
            console.error('Failed to update payment status:', err);
            setError('Failed to update payment status');
        }
    };

    const deleteSale = async (saleId) => {
        if (window.confirm('Are you sure you want to delete this sale record?')) {
            try {
                await axios.delete(`${API_BASE}/sales/${saleId}`);
                fetchData();
                setError('');
            } catch (err) {
                console.error('Failed to delete sale:', err);
                setError('Failed to delete sale record');
            }
        }
    };

    const updatePaymentAmount = async (saleId, paidAmount) => {
        try {
            // Find the sale record
            const sale = sales.find(s => s.sales_id === saleId);
            if (!sale) return;

            // Calculate new balance and payment status
            const newPaidAmount = parseFloat(paidAmount) || 0;
            const grandTotal = parseFloat(sale.grand_total) || 0;
            const balance = grandTotal - newPaidAmount;
            
            let newStatus;
            if (newPaidAmount <= 0) {
                newStatus = 'Unpaid';
            } else if (newPaidAmount >= grandTotal) {
                newStatus = 'Paid';
            } else {
                newStatus = 'Partial';
            }

            // Update local state immediately for instant feedback
            setSales(prevSales => 
                prevSales.map(s => 
                    s.sales_id === saleId 
                        ? { ...s, paid_amount: newPaidAmount, balance: balance, payment_status: newStatus }
                        : s
                )
            );

            // Update backend
            await axios.put(`${API_BASE}/sales/${saleId}`, {
                ...sale,
                paid_amount: newPaidAmount,
                balance: balance,
                payment_status: newStatus
            });

            // Refresh data from server to ensure consistency
            fetchData();
        } catch (err) {
            console.error('Failed to update payment amount:', err);
            setError('Failed to update payment amount');
        }
    };
    const validationSchema = Yup.object({
        customer_id: Yup.string().required('Customer name is required').min(2, 'Customer name must be at least 2 characters'),
        invoice_number: Yup.string().required('Invoice number is required').matches(/^[A-Z0-9\-]+$/, 'Invoice should contain only uppercase letters, numbers, and hyphens'),
        date: Yup.date().required('Date is required').max(new Date(), 'Date cannot be in the future'),
        product_name: Yup.string().required('Product name is required'),
        product_type: Yup.string().required('Product type is required').oneOf(['Finished Product', 'Yarn', 'Raw Material'], 'Invalid product type'),
        quantity: Yup.number().typeError('Must be a number').positive('Must be positive').required('Quantity is required').min(1, 'Minimum quantity is 1').max(10000, 'Maximum quantity is 10000'),
        unit: Yup.string().required('Unit is required').oneOf(['KG', 'TONS', 'METERS', 'UNITS'], 'Invalid unit'),
        rate: Yup.number().typeError('Must be a number').positive('Must be positive').required('Rate is required').min(0.01, 'Minimum rate is 0.01').max(10000, 'Maximum rate is 10000'),
        payment_status: Yup.string().required('Payment status is required').oneOf(['Paid', 'Unpaid', 'Partial'], 'Invalid payment status'),
        paid_amount: Yup.number().typeError('Must be a number').min(0, 'Paid amount cannot be negative'),
        remarks: Yup.string().max(500, 'Remarks cannot exceed 500 characters')
    });

    const formik = useFormik({
        initialValues: {
            customer_id: '',
            invoice_number: '',
            date: new Date().toISOString().split('T')[0],
            product_name: '',
            product_type: 'Finished Product',
            quantity: '',
            unit: 'KG',
            rate: '',
            total_amount: 0,
            cgst: 0,
            sgst: 0,
            igst: 0,
            tax_amount: 0,
            grand_total: 0,
            payment_status: 'Unpaid',
            paid_amount: 0,
            balance: 0,
            remarks: ''
        },
        validationSchema,
        onSubmit: async (values, { resetForm }) => {
            try {
                await axios.post(`${API_BASE}/sales/`, {
                    ...values,
                    quantity: parseFloat(values.quantity),
                    rate: parseFloat(values.rate),
                    date: new Date(values.date).toISOString()
                });
                setOpen(false);
                setError('');
                fetchData();
                resetForm();
            } catch (err) {
                console.error(err);
                setError('Failed to save sale. Please try again.');
            }
        }
    });

    const handleCustomChange = (e) => {
        formik.handleChange(e);
        const { name, value } = e.target;
        if (name === 'quantity' || name === 'rate') {
            const qty = parseFloat(name === 'quantity' ? value : formik.values.quantity) || 0;
            const rate = parseFloat(name === 'rate' ? value : formik.values.rate) || 0;
            const total = qty * rate;
            formik.setFieldValue('total_amount', total);
            formik.setFieldValue('grand_total', total);
            // Update balance based on new total and current paid amount
            const currentPaid = parseFloat(formik.values.paid_amount) || 0;
            formik.setFieldValue('balance', total - currentPaid);
        } else if (name === 'paid_amount') {
            // Update balance when paid amount changes
            const paidAmount = parseFloat(value) || 0;
            const grandTotal = parseFloat(formik.values.grand_total) || 0;
            formik.setFieldValue('balance', grandTotal - paidAmount);
        }
    };

    const handleClose = () => {
        setOpen(false);
        formik.resetForm();
        setError('');
    };

    return (
        <Box>
            <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 4 }}>
                <Box>
                    <Typography variant="h4" sx={{ fontWeight: 700 }}>Sales</Typography>
                    <Typography variant="body2" color="textSecondary">Manage customer billings and order fulfillments</Typography>
                </Box>
                <Button
                    variant="contained"
                    startIcon={<AddIcon />}
                    onClick={() => setOpen(true)}
                    sx={{ borderRadius: 2, px: 3, bgcolor: '#4caf50', '&:hover': { bgcolor: '#388e3c' } }}
                >
                    Record Sale
                </Button>
            </Stack>

            <TableContainer component={Paper} sx={{ borderRadius: 3, boxShadow: '0 4px 20px rgba(0,0,0,0.05)' }}>
                <Table>
                    <TableHead sx={{ bgcolor: '#f8fafc' }}>
                        <TableRow>
                            <TableCell>Date</TableCell>
                            <TableCell>Invoice</TableCell>
                            <TableCell>Customer</TableCell>
                            <TableCell>Product</TableCell>
                            <TableCell align="right">Quantity</TableCell>
                            <TableCell align="right">Total</TableCell>
                            <TableCell align="right">Paid Amount</TableCell>
                            <TableCell align="right">Balance</TableCell>
                            <TableCell>Status</TableCell>
                            <TableCell>Actions</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {sales.map((row) => (
                            <TableRow key={row.sales_id} hover>
                                <TableCell>{new Date(row.date).toLocaleDateString()}</TableCell>
                                <TableCell>
                                    <Stack direction="row" spacing={1} alignItems="center">
                                        <ReceiptIcon fontSize="small" color="action" />
                                        <Typography variant="body2">{row.invoice_number}</Typography>
                                    </Stack>
                                </TableCell>
                                <TableCell>{row.customer_id}</TableCell>
                                <TableCell>{row.product_name}</TableCell>
                                <TableCell align="right">{row.quantity} {row.unit}</TableCell>
                                <TableCell align="right" sx={{ fontWeight: 600 }}>₹{row.grand_total.toLocaleString()}</TableCell>
                                <TableCell align="right">
                                    <TextField
                                        type="number"
                                        size="small"
                                        value={row.paid_amount || 0}
                                        onChange={(e) => updatePaymentAmount(row.sales_id, e.target.value)}
                                        sx={{ width: 120 }}
                                        InputProps={{
                                            startAdornment: '₹',
                                            style: { textAlign: 'right' }
                                        }}
                                    />
                                </TableCell>
                                <TableCell align="right" sx={{ fontWeight: 600, color: row.balance > 0 ? 'error.main' : 'success.main' }}>
                                    ₹{(row.balance || 0).toLocaleString()}
                                </TableCell>
                                <TableCell>
                                    {editingStatus === row.sales_id ? (
                                        <Stack direction="row" spacing={1} alignItems="center">
                                            <Select
                                                value={row.payment_status}
                                                onChange={(e) => updatePaymentStatus(row.sales_id, e.target.value)}
                                                size="small"
                                                sx={{ minWidth: 120 }}
                                            >
                                                <MenuItem value="Paid">Paid</MenuItem>
                                                <MenuItem value="Unpaid">Unpaid</MenuItem>
                                                <MenuItem value="Partial">Partially Paid</MenuItem>
                                            </Select>
                                            <IconButton
                                                size="small"
                                                onClick={() => setEditingStatus(null)}
                                                color="error"
                                            >
                                                ✕
                                            </IconButton>
                                        </Stack>
                                    ) : (
                                        <Stack direction="row" spacing={1} alignItems="center">
                                            <Chip
                                                label={row.payment_status}
                                                color={row.payment_status === 'Paid' ? 'success' : 'warning'}
                                                size="small"
                                                sx={{ borderRadius: 1, cursor: 'pointer' }}
                                                onClick={() => setEditingStatus(row.sales_id)}
                                            />
                                            <IconButton
                                                size="small"
                                                onClick={() => setEditingStatus(row.sales_id)}
                                                sx={{ p: 0.5 }}
                                            >
                                                <EditIcon fontSize="small" />
                                            </IconButton>
                                        </Stack>
                                    )}
                                </TableCell>
                                <TableCell>
                                    <IconButton
                                        size="small"
                                        onClick={() => deleteSale(row.sales_id)}
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

            <Dialog open={open} onClose={handleClose} maxWidth="md" fullWidth>
                <DialogTitle>Record New Sale</DialogTitle>
                <form onSubmit={formik.handleSubmit}>
                    <DialogContent dividers>
                        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
                        <Stack spacing={3} sx={{ mt: 1 }}>
                            <Stack direction="row" spacing={2}>
                                <TextField
                                    name="customer_id"
                                    label="Customer Name"
                                    fullWidth
                                    value={formik.values.customer_id}
                                    onChange={formik.handleChange}
                                    onBlur={formik.handleBlur}
                                    error={formik.touched.customer_id && Boolean(formik.errors.customer_id)}
                                    helperText={formik.touched.customer_id && formik.errors.customer_id}
                                    placeholder="Enter customer name manually"
                                />
                                <TextField name="invoice_number" label="Invoice Number" fullWidth value={formik.values.invoice_number} onChange={formik.handleChange} onBlur={formik.handleBlur} error={formik.touched.invoice_number && Boolean(formik.errors.invoice_number)} helperText={formik.touched.invoice_number && formik.errors.invoice_number} />
                            </Stack>
                            <Stack direction="row" spacing={2}>
                                <TextField name="date" label="Date" type="date" value={formik.values.date} fullWidth onChange={formik.handleChange} onBlur={formik.handleBlur} error={formik.touched.date && Boolean(formik.errors.date)} helperText={formik.touched.date && formik.errors.date} InputLabelProps={{ shrink: true }} />
                                <TextField
                                    select
                                    name="product_name"
                                    label="Product Name"
                                    fullWidth
                                    value={formik.values.product_name}
                                    onChange={formik.handleChange}
                                    onBlur={formik.handleBlur}
                                    error={formik.touched.product_name && Boolean(formik.errors.product_name)}
                                    helperText={formik.touched.product_name && formik.errors.product_name}
                                >
                                    {productTypes.map((type) => (
                                        <MenuItem key={type} value={type}>{type}</MenuItem>
                                    ))}
                                </TextField>
                            </Stack>
                            <Stack direction="row" spacing={2}>
                                <TextField name="quantity" label="Quantity" type="number" fullWidth value={formik.values.quantity} onChange={handleCustomChange} onBlur={formik.handleBlur} error={formik.touched.quantity && Boolean(formik.errors.quantity)} helperText={formik.touched.quantity && formik.errors.quantity} />
                                <TextField name="unit" label="Unit" fullWidth value={formik.values.unit} onChange={formik.handleChange} onBlur={formik.handleBlur} error={formik.touched.unit && Boolean(formik.errors.unit)} helperText={formik.touched.unit && formik.errors.unit} />
                                <TextField name="rate" label="Rate (₹)" type="number" fullWidth value={formik.values.rate} onChange={handleCustomChange} onBlur={formik.handleBlur} error={formik.touched.rate && Boolean(formik.errors.rate)} helperText={formik.touched.rate && formik.errors.rate} />
                            </Stack>
                            <Stack direction="row" spacing={2}>
                                <TextField
                                    select
                                    name="payment_status"
                                    label="Payment Status"
                                    fullWidth
                                    value={formik.values.payment_status}
                                    onChange={formik.handleChange}
                                    onBlur={formik.handleBlur}
                                    error={formik.touched.payment_status && Boolean(formik.errors.payment_status)}
                                    helperText={formik.touched.payment_status && formik.errors.payment_status}
                                    sx={{ bgcolor: 'yellow' }}  // Temporary highlight for visibility
                                >
                                    <MenuItem value="Paid">Paid</MenuItem>
                                    <MenuItem value="Unpaid">Unpaid</MenuItem>
                                    <MenuItem value="Partial">Partially Paid</MenuItem>
                                </TextField>
                                <TextField name="paid_amount" label="Paid Amount" type="number" fullWidth value={formik.values.paid_amount} onChange={handleCustomChange} onBlur={formik.handleBlur} error={formik.touched.paid_amount && Boolean(formik.errors.paid_amount)} helperText={formik.touched.paid_amount && formik.errors.paid_amount} />
                            </Stack>
                            <Paper sx={{ p: 2, bgcolor: '#f0fff4' }}>
                                <Typography variant="h6">Total Amount: ₹{formik.values.total_amount.toLocaleString()}</Typography>
                                <Typography variant="body2" color="textSecondary">Balance: ₹{formik.values.balance.toLocaleString()}</Typography>
                            </Paper>
                        </Stack>
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={handleClose}>Cancel</Button>
                        <Button variant="contained" type="submit" color="success">Save Sale</Button>
                    </DialogActions>
                </form>
            </Dialog>
        </Box>
    );
};

export default Sales;
