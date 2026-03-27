import React, { useState, useEffect } from 'react';
import {
    Box, Typography, Paper, Table, TableBody, TableCell,
    TableContainer, TableHead, TableRow, Alert
} from '@mui/material';
import axios from 'axios';

const Inventory = () => {
    const [inventory, setInventory] = useState([]);

    useEffect(() => {
        axios.get('http://127.0.0.1:8000/api/inventory')
            .then(res => setInventory(res.data))
            .catch(err => console.error(err));
    }, []);

    return (
        <Box>
            <Typography variant="h4" gutterBottom>Inventory</Typography>
            <TableContainer component={Paper}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Item Name</TableCell>
                            <TableCell>Type</TableCell>
                            <TableCell align="right">Opening Stock</TableCell>
                            <TableCell align="right">Stock In</TableCell>
                            <TableCell align="right">Stock Out</TableCell>
                            <TableCell align="right">Closing Stock</TableCell>
                            <TableCell>Last Updated</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {inventory.map((row) => (
                            <TableRow key={row.inventory_id}>
                                <TableCell>{row.item_name}</TableCell>
                                <TableCell>{row.item_type}</TableCell>
                                <TableCell align="right">{row.opening_stock}</TableCell>
                                <TableCell align="right" sx={{ color: 'success.main' }}>+{row.stock_in}</TableCell>
                                <TableCell align="right" sx={{ color: 'error.main' }}>-{row.stock_out}</TableCell>
                                <TableCell align="right" sx={{ fontWeight: 'bold' }}>{row.closing_stock}</TableCell>
                                <TableCell>{new Date(row.last_updated).toLocaleString()}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
            {inventory.filter(i => i.closing_stock < 1000).length > 0 && (
                <Alert severity="warning" sx={{ mt: 2 }}>
                    Some items are reaching low stock levels!
                </Alert>
            )}
        </Box>
    );
};

export default Inventory;
