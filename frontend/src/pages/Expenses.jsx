import React, { useState, useEffect } from 'react';
import {
    Box, Typography, Paper, Table, TableBody, TableCell,
    TableContainer, TableHead, TableRow, Button, Dialog,
    DialogTitle, DialogContent, DialogActions, TextField,
    Stack, IconButton, MenuItem, Grid, Alert
} from '@mui/material';
import { Add as AddIcon, ReceiptLong as ExpenseIcon, Delete as DeleteIcon } from '@mui/icons-material';
import axios from 'axios';
import { useFormik } from 'formik';
import * as Yup from 'yup';

const API_BASE = 'http://127.0.0.1:8000/api';

const Expenses = () => {
    const [expenses, setExpenses] = useState([]);
    const [open, setOpen] = useState(false);
    const [error, setError] = useState('');
    const fetchExpenses = async () => {
        try {
            const res = await axios.get(`${API_BASE}/expenses`);
            setExpenses(res.data);
        } catch (err) {
            console.error(err);
        }
    };

    useEffect(() => {
        fetchExpenses();
    }, []);

    const validationSchema = Yup.object({
        expense_type: Yup.string().required('Expense type is required').min(2, 'Type must be at least 2 characters').max(50, 'Type cannot exceed 50 characters'),
        category: Yup.string().required('Category is required').oneOf(['Direct', 'Indirect'], 'Invalid category'),
        amount: Yup.number().typeError('Amount must be a number').positive('Amount must be greater than zero').required('Amount is required').min(0.01, 'Minimum amount is 0.01').max(1000000, 'Maximum amount is 10,00,000'),
        date: Yup.date().required('Date is required').max(new Date(), 'Date cannot be in the future'),
        vendor_name: Yup.string().max(100, 'Vendor name cannot exceed 100 characters'),
        payment_mode: Yup.string().required('Payment mode is required').oneOf(['Cash', 'Bank', 'UPI', 'Cheque', 'Credit Card', 'Debit Card'], 'Invalid payment mode'),
        description: Yup.string().required('Description is required').min(5, 'Description must be at least 5 characters').max(500, 'Description cannot exceed 500 characters'),
        bill_number: Yup.string().max(50, 'Bill number cannot exceed 50 characters'),
        payment_reference: Yup.string().max(100, 'Payment reference cannot exceed 100 characters')
    });

    const formik = useFormik({
        initialValues: {
            expense_type: '',
            category: 'Indirect',
            amount: '',
            date: new Date().toISOString().split('T')[0],
            description: '',
            vendor_name: '',
            payment_mode: 'Cash'
        },
        validationSchema: validationSchema,
        onSubmit: async (values, { resetForm }) => {
            try {
                await axios.post(`${API_BASE}/expenses`, {
                    ...values,
                    amount: parseFloat(values.amount),
                    date: new Date(values.date).toISOString()
                });
                setOpen(false);
                setError('');
                fetchExpenses();
                resetForm({
                    values: {
                        expense_type: '',
                        category: 'Indirect',
                        amount: '',
                        date: new Date().toISOString().split('T')[0],
                        description: '',
                        vendor_name: '',
                        payment_mode: 'Cash'
                    }
                });
            } catch (err) {
                console.error(err);
                setError('Failed to save expense');
            }
        },
    });

    const handleClose = () => {
        setOpen(false);
        formik.resetForm({
            values: {
                expense_type: '',
                category: 'Indirect',
                amount: '',
                date: new Date().toISOString().split('T')[0],
                description: '',
                vendor_name: '',
                payment_mode: 'Cash'
            }
        });
        setError('');
    };

    const handleDelete = async (id) => {
        try {
            await axios.delete(`${API_BASE}/expenses/${id}`);
            fetchExpenses();
        } catch (err) {
            console.error(err);
        }
    };

    return (
        <Box sx={{ flexGrow: 1 }}>
            <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 4 }}>
                <Box>
                    <Typography variant="h4" sx={{ fontWeight: 700 }}>Expenses</Typography>
                    <Typography variant="body2" color="textSecondary">Track your daily business expenditures</Typography>
                </Box>
                <Button
                    variant="contained"
                    startIcon={<AddIcon />}
                    onClick={() => setOpen(true)}
                    sx={{ borderRadius: 2, px: 3, bgcolor: '#ff9800', '&:hover': { bgcolor: '#f57c00' } }}
                >
                    Record Expense
                </Button>
            </Stack>

            <Grid container spacing={3} sx={{ mb: 4 }}>
                <Grid item xs={12} md={4}>
                    <Paper sx={{ p: 2, textAlign: 'center', bgcolor: '#fff4e5' }}>
                        <Typography color="textSecondary" variant="overline">Total Expenses</Typography>
                        <Typography variant="h4" color="warning.main">
                            ₹{expenses.reduce((sum, e) => sum + e.amount, 0).toLocaleString()}
                        </Typography>
                    </Paper>
                </Grid>
            </Grid>

            <TableContainer component={Paper} sx={{ borderRadius: 3, boxShadow: '0 4px 20px rgba(0,0,0,0.05)' }}>
                <Table>
                    <TableHead sx={{ bgcolor: '#f8fafc' }}>
                        <TableRow>
                            <TableCell>Date</TableCell>
                            <TableCell>Type</TableCell>
                            <TableCell>Vendor</TableCell>
                            <TableCell>Category</TableCell>
                            <TableCell>Mode</TableCell>
                            <TableCell align="right">Amount</TableCell>
                            <TableCell align="right">Actions</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {expenses.map((row) => (
                            <TableRow key={row.expense_id} hover>
                                <TableCell>{new Date(row.date).toLocaleDateString()}</TableCell>
                                <TableCell>
                                    <Typography variant="subtitle2">{row.expense_type}</Typography>
                                    <Typography variant="caption" color="textSecondary">{row.description}</Typography>
                                </TableCell>
                                <TableCell>{row.vendor_name || '-'}</TableCell>
                                <TableCell>{row.category}</TableCell>
                                <TableCell>{row.payment_mode}</TableCell>
                                <TableCell align="right" sx={{ fontWeight: 600 }}>₹{row.amount.toLocaleString()}</TableCell>
                                <TableCell align="right">
                                    <IconButton size="small" color="error" onClick={() => handleDelete(row.expense_id)}>
                                        <DeleteIcon fontSize="small" />
                                    </IconButton>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>

            <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
                <DialogTitle>Record New Expense</DialogTitle>
                <form onSubmit={formik.handleSubmit}>
                    <DialogContent dividers>
                        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
                        <Stack spacing={2} sx={{ mt: 1 }}>
                            <TextField name="expense_type" label="Expense Type (e.g. Rent, Salary)" fullWidth value={formik.values.expense_type} onChange={formik.handleChange} onBlur={formik.handleBlur} error={formik.touched.expense_type && Boolean(formik.errors.expense_type)} helperText={formik.touched.expense_type && formik.errors.expense_type} />
                            <TextField
                                select
                                name="category"
                                label="Category"
                                value={formik.values.category}
                                fullWidth
                                onChange={formik.handleChange}
                                onBlur={formik.handleBlur}
                                error={formik.touched.category && Boolean(formik.errors.category)}
                                helperText={formik.touched.category && formik.errors.category}
                            >
                                <MenuItem value="Direct">Direct</MenuItem>
                                <MenuItem value="Indirect">Indirect</MenuItem>
                            </TextField>
                            <TextField name="amount" label="Amount (₹)" type="number" fullWidth value={formik.values.amount} onChange={formik.handleChange} onBlur={formik.handleBlur} error={formik.touched.amount && Boolean(formik.errors.amount)} helperText={formik.touched.amount && formik.errors.amount} />
                            <TextField name="date" label="Date" type="date" value={formik.values.date} fullWidth onChange={formik.handleChange} onBlur={formik.handleBlur} error={formik.touched.date && Boolean(formik.errors.date)} helperText={formik.touched.date && formik.errors.date} InputLabelProps={{ shrink: true }} />
                            <TextField name="vendor_name" label="Vendor Name" fullWidth value={formik.values.vendor_name} onChange={formik.handleChange} onBlur={formik.handleBlur} error={formik.touched.vendor_name && Boolean(formik.errors.vendor_name)} helperText={formik.touched.vendor_name && formik.errors.vendor_name} />
                            <TextField
                                select
                                name="payment_mode"
                                label="Payment Mode"
                                value={formik.values.payment_mode}
                                fullWidth
                                onChange={formik.handleChange}
                                onBlur={formik.handleBlur}
                                error={formik.touched.payment_mode && Boolean(formik.errors.payment_mode)}
                                helperText={formik.touched.payment_mode && formik.errors.payment_mode}
                            >
                                <MenuItem value="Cash">Cash</MenuItem>
                                <MenuItem value="Bank">Bank</MenuItem>
                                <MenuItem value="UPI">UPI</MenuItem>
                            </TextField>
                            <TextField name="description" label="Description" fullWidth multiline rows={2} value={formik.values.description} onChange={formik.handleChange} onBlur={formik.handleBlur} error={formik.touched.description && Boolean(formik.errors.description)} helperText={formik.touched.description && formik.errors.description} />
                        </Stack>
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={handleClose}>Cancel</Button>
                        <Button variant="contained" type="submit" sx={{ bgcolor: '#ff9800' }}>Save Expense</Button>
                    </DialogActions>
                </form>
            </Dialog>
        </Box>
    );
};

export default Expenses;
