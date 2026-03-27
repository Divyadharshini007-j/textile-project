import React, { useState, useEffect } from 'react';
import {
    Box, Typography, Paper, Table, TableBody, TableCell,
    TableContainer, TableHead, TableRow, Button, Grid, Card, CardContent,
    Dialog, DialogTitle, DialogContent, DialogActions, TextField, Stack, MenuItem, Alert
} from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import axios from 'axios';
import { useFormik } from 'formik';
import * as Yup from 'yup';

const API_BASE = 'http://127.0.0.1:8000/api';

const Conversions = () => {
    const [conversions, setConversions] = useState([]);
    const [open, setOpen] = useState(false);
    const [error, setError] = useState('');

    const validationSchema = Yup.object({
        date: Yup.date().required('Date is required').max(new Date(), 'Date cannot be in the future'),
        input_yarn_type: Yup.string().required('Input yarn type is required'),
        input_quantity: Yup.number().typeError('Must be a number').positive('Must be positive').required('Input quantity is required').min(1, 'Minimum quantity is 1').max(10000, 'Maximum quantity is 10000'),
        input_cost: Yup.number().typeError('Must be a number').positive('Must be positive').required('Input cost is required').min(0.01, 'Minimum cost is 0.01'),
        output_product: Yup.string().required('Output product is required'),
        output_quantity: Yup.number().typeError('Must be a number').positive('Must be positive').required('Output quantity is required').min(1, 'Minimum quantity is 1').max(10000, 'Maximum quantity is 10000'),
        labor_cost: Yup.number().typeError('Must be a number').min(0, 'Labor cost cannot be negative').required('Labor cost is required'),
        overhead_cost: Yup.number().typeError('Must be a number').min(0, 'Overhead cost cannot be negative').required('Overhead cost is required'),
        wastage: Yup.number().typeError('Must be a number').min(0, 'Wastage cannot be negative').max(50, 'Wastage cannot exceed 50%').required('Wastage is required'),
        remarks: Yup.string().max(500, 'Remarks cannot exceed 500 characters')
    });

    const formik = useFormik({
        initialValues: {
            date: new Date().toISOString().split('T')[0],
            input_yarn_type: '',
            input_quantity: '',
            input_cost: '',
            output_product: '',
            output_quantity: '',
            labor_cost: '',
            overhead_cost: '',
            wastage: '',
            remarks: ''
        },
        validationSchema,
        onSubmit: async (values, { resetForm }) => {
            try {
                const total_conversion_cost = parseFloat(values.labor_cost) + parseFloat(values.overhead_cost);
                await axios.post(`${API_BASE}/conversions/`, {
                    ...values,
                    input_quantity: parseFloat(values.input_quantity),
                    input_cost: parseFloat(values.input_cost),
                    output_quantity: parseFloat(values.output_quantity),
                    labor_cost: parseFloat(values.labor_cost),
                    overhead_cost: parseFloat(values.overhead_cost),
                    total_conversion_cost: total_conversion_cost,
                    wastage: parseFloat(values.wastage),
                    date: new Date(values.date).toISOString()
                });
                setOpen(false);
                setError('');
                fetchData();
                resetForm();
            } catch (err) {
                console.error(err);
                setError('Failed to save conversion. Please try again.');
            }
        }
    });

    const fetchData = async () => {
        try {
            const res = await axios.get(`${API_BASE}/conversions/`);
            setConversions(res.data);
        } catch (err) {
            console.error(err);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    const handleClose = () => {
        setOpen(false);
        formik.resetForm();
        setError('');
    };

    return (
        <Box>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                <Typography variant="h4">Conversion Tracking</Typography>
                <Button variant="contained" startIcon={<AddIcon />} onClick={() => setOpen(true)}>Record New Conversion</Button>
            </Box>

            <Grid container spacing={2} sx={{ mb: 4 }}>
                <Grid item xs={12} md={4}>
                    <Card sx={{ bgcolor: 'info.light' }}>
                        <CardContent>
                            <Typography variant="h6">Total Input Yarn</Typography>
                            <Typography variant="h4">{conversions.reduce((acc, curr) => acc + curr.input_quantity, 0).toLocaleString()} KG</Typography>
                        </CardContent>
                    </Card>
                </Grid>
                <Grid item xs={12} md={4}>
                    <Card sx={{ bgcolor: 'success.light' }}>
                        <CardContent>
                            <Typography variant="h6">Total Fabric Produced</Typography>
                            <Typography variant="h4">{conversions.reduce((acc, curr) => acc + curr.output_quantity, 0).toLocaleString()} Units</Typography>
                        </CardContent>
                    </Card>
                </Grid>
                <Grid item xs={12} md={4}>
                    <Card sx={{ bgcolor: 'warning.light' }}>
                        <CardContent>
                            <Typography variant="h6">Avg. Wastage</Typography>
                            <Typography variant="h4">
                                {conversions.length > 0 ? (conversions.reduce((acc, curr) => acc + curr.wastage, 0) / conversions.length).toFixed(2) : 0} %
                            </Typography>
                        </CardContent>
                    </Card>
                </Grid>
            </Grid>

            <TableContainer component={Paper}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Date</TableCell>
                            <TableCell>Input Yarn</TableCell>
                            <TableCell align="right">Input Qty</TableCell>
                            <TableCell>Output Product</TableCell>
                            <TableCell align="right">Output Qty</TableCell>
                            <TableCell align="right">Cost</TableCell>
                            <TableCell align="right">Wastage</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {conversions.map((row) => (
                            <TableRow key={row.conversion_id}>
                                <TableCell>{new Date(row.date).toLocaleDateString()}</TableCell>
                                <TableCell>{row.input_yarn_type}</TableCell>
                                <TableCell align="right">{row.input_quantity} KG</TableCell>
                                <TableCell>{row.output_product}</TableCell>
                                <TableCell align="right">{row.output_quantity} Units</TableCell>
                                <TableCell align="right">₹{row.total_conversion_cost.toLocaleString()}</TableCell>
                                <TableCell align="right">{row.wastage}%</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>

            <Dialog open={open} onClose={handleClose} maxWidth="md" fullWidth>
                <DialogTitle>Record New Conversion</DialogTitle>
                <form onSubmit={formik.handleSubmit}>
                    <DialogContent dividers>
                        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
                        <Stack spacing={3}>
                            <TextField
                                name="date"
                                label="Date"
                                type="date"
                                fullWidth
                                value={formik.values.date}
                                onChange={formik.handleChange}
                                onBlur={formik.handleBlur}
                                error={formik.touched.date && Boolean(formik.errors.date)}
                                helperText={formik.touched.date && formik.errors.date}
                                InputLabelProps={{ shrink: true }}
                            />
                            <Stack direction="row" spacing={2}>
                                <TextField
                                    name="input_yarn_type"
                                    label="Input Yarn Type"
                                    fullWidth
                                    value={formik.values.input_yarn_type}
                                    onChange={formik.handleChange}
                                    onBlur={formik.handleBlur}
                                    error={formik.touched.input_yarn_type && Boolean(formik.errors.input_yarn_type)}
                                    helperText={formik.touched.input_yarn_type && formik.errors.input_yarn_type}
                                />
                                <TextField
                                    name="input_quantity"
                                    label="Input Quantity (KG)"
                                    type="number"
                                    fullWidth
                                    value={formik.values.input_quantity}
                                    onChange={formik.handleChange}
                                    onBlur={formik.handleBlur}
                                    error={formik.touched.input_quantity && Boolean(formik.errors.input_quantity)}
                                    helperText={formik.touched.input_quantity && formik.errors.input_quantity}
                                />
                            </Stack>
                            <Stack direction="row" spacing={2}>
                                <TextField
                                    name="input_cost"
                                    label="Input Cost per KG"
                                    type="number"
                                    fullWidth
                                    value={formik.values.input_cost}
                                    onChange={formik.handleChange}
                                    onBlur={formik.handleBlur}
                                    error={formik.touched.input_cost && Boolean(formik.errors.input_cost)}
                                    helperText={formik.touched.input_cost && formik.errors.input_cost}
                                />
                                <TextField
                                    name="output_product"
                                    label="Output Product"
                                    fullWidth
                                    value={formik.values.output_product}
                                    onChange={formik.handleChange}
                                    onBlur={formik.handleBlur}
                                    error={formik.touched.output_product && Boolean(formik.errors.output_product)}
                                    helperText={formik.touched.output_product && formik.errors.output_product}
                                />
                            </Stack>
                            <Stack direction="row" spacing={2}>
                                <TextField
                                    name="output_quantity"
                                    label="Output Quantity (Units)"
                                    type="number"
                                    fullWidth
                                    value={formik.values.output_quantity}
                                    onChange={formik.handleChange}
                                    onBlur={formik.handleBlur}
                                    error={formik.touched.output_quantity && Boolean(formik.errors.output_quantity)}
                                    helperText={formik.touched.output_quantity && formik.errors.output_quantity}
                                />
                                <TextField
                                    name="wastage"
                                    label="Wastage (%)"
                                    type="number"
                                    fullWidth
                                    value={formik.values.wastage}
                                    onChange={formik.handleChange}
                                    onBlur={formik.handleBlur}
                                    error={formik.touched.wastage && Boolean(formik.errors.wastage)}
                                    helperText={formik.touched.wastage && formik.errors.wastage}
                                />
                            </Stack>
                            <Stack direction="row" spacing={2}>
                                <TextField
                                    name="labor_cost"
                                    label="Labor Cost"
                                    type="number"
                                    fullWidth
                                    value={formik.values.labor_cost}
                                    onChange={formik.handleChange}
                                    onBlur={formik.handleBlur}
                                    error={formik.touched.labor_cost && Boolean(formik.errors.labor_cost)}
                                    helperText={formik.touched.labor_cost && formik.errors.labor_cost}
                                />
                                <TextField
                                    name="overhead_cost"
                                    label="Overhead Cost"
                                    type="number"
                                    fullWidth
                                    value={formik.values.overhead_cost}
                                    onChange={formik.handleChange}
                                    onBlur={formik.handleBlur}
                                    error={formik.touched.overhead_cost && Boolean(formik.errors.overhead_cost)}
                                    helperText={formik.touched.overhead_cost && formik.errors.overhead_cost}
                                />
                            </Stack>
                            <TextField
                                name="remarks"
                                label="Remarks"
                                multiline
                                rows={3}
                                fullWidth
                                value={formik.values.remarks}
                                onChange={formik.handleChange}
                                onBlur={formik.handleBlur}
                                error={formik.touched.remarks && Boolean(formik.errors.remarks)}
                                helperText={formik.touched.remarks && formik.errors.remarks}
                            />
                        </Stack>
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={handleClose}>Cancel</Button>
                        <Button variant="contained" type="submit">Save Conversion</Button>
                    </DialogActions>
                </form>
            </Dialog>
        </Box>
    );
};

export default Conversions;
