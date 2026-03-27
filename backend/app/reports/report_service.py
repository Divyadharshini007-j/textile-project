from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from sqlalchemy.orm import Session
from app.models import models
from sqlalchemy import func
from datetime import datetime

class ReportService:
    @staticmethod
    def generate_profit_loss_pdf(db: Session):
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        
        # Header
        p.setFillColorRGB(0.13, 0.58, 0.95)
        p.rect(0, 750, 612, 50, fill=1, stroke=0)
        p.setFillColorRGB(1, 1, 1)
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, 770, "PROFIT & LOSS STATEMENT")
        p.setFont("Helvetica", 10)
        p.drawString(100, 755, "Yarn Trading Company")
        
        # Reset color
        p.setFillColorRGB(0, 0, 0)
        p.setFont("Helvetica", 12)
        p.drawString(100, 720, f"Generated on: {datetime.now().strftime('%d %B %Y, %I:%M %p')}")
        
        # Get detailed data
        sales = db.query(models.Sale).all()
        purchases = db.query(models.Purchase).all()
        expenses = db.query(models.Expense).all()
        inventory = db.query(models.Inventory).all()
        
        total_sales = sum(sale.grand_total or 0 for sale in sales)
        total_purchases = sum(purchase.grand_total or 0 for purchase in purchases)
        total_expenses = sum(expense.amount or 0 for expense in expenses)
        total_inventory_value = sum(item.total_value or 0 for item in inventory)
        net_profit = (total_sales + total_inventory_value) - (total_purchases + total_expenses)
        
        # Revenue Section
        y = 680
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, y, "REVENUE")
        p.setFont("Helvetica", 11)
        y -= 25
        p.drawString(120, y, f"Total Sales Revenue: ₹{total_sales:,.2f}")
        y -= 20
        p.drawString(120, y, f"Current Inventory Value: ₹{total_inventory_value:,.2f}")
        y -= 20
        p.setFont("Helvetica-Bold", 12)
        p.drawString(120, y, f"Total Revenue: ₹{(total_sales + total_inventory_value):,.2f}")
        
        # Expenses Section
        y -= 35
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, y, "EXPENSES")
        p.setFont("Helvetica", 11)
        y -= 25
        p.drawString(120, y, f"Cost of Goods Sold (Purchases): ₹{total_purchases:,.2f}")
        y -= 20
        p.drawString(120, y, f"Operating Expenses: ₹{total_expenses:,.2f}")
        y -= 20
        p.setFont("Helvetica-Bold", 12)
        p.drawString(120, y, f"Total Expenses: ₹{(total_purchases + total_expenses):,.2f}")
        
        # Profit/Loss Section
        y -= 35
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, y, "PROFIT / LOSS")
        y -= 25
        p.setFont("Helvetica-Bold", 12)
        if net_profit >= 0:
            p.setFillColorRGB(0, 0.5, 0)
            p.drawString(120, y, f"NET PROFIT: ₹{net_profit:,.2f}")
            p.setFont("Helvetica", 10)
            p.drawString(350, y, "✓ PROFITABLE")
        else:
            p.setFillColorRGB(0.8, 0, 0)
            p.drawString(120, y, f"NET LOSS: ₹{abs(net_profit):,.2f}")
            p.setFont("Helvetica", 10)
            p.drawString(350, y, "✗ LOSS")
        
        # Summary Statistics
        p.setFillColorRGB(0, 0, 0)
        y -= 40
        p.setFont("Helvetica-Bold", 12)
        p.drawString(100, y, "SUMMARY STATISTICS")
        p.setFont("Helvetica", 10)
        y -= 20
        p.drawString(120, y, f"Number of Sales: {len(sales)}")
        y -= 15
        p.drawString(120, y, f"Number of Purchases: {len(purchases)}")
        y -= 15
        p.drawString(120, y, f"Number of Expenses: {len(expenses)}")
        y -= 15
        p.drawString(120, y, f"Inventory Items: {len(inventory)}")
        
        # Detailed Sales (Top 5)
        if sales:
            y -= 25
            p.setFont("Helvetica-Bold", 12)
            p.drawString(100, y, "RECENT SALES (Top 5)")
            p.setFont("Helvetica", 9)
            y -= 20
            p.drawString(100, y, "Date")
            p.drawString(200, y, "Customer")
            p.drawString(400, y, "Amount")
            y -= 15
            for sale in sorted(sales, key=lambda x: x.date or '', reverse=True)[:5]:
                if y < 100:
                    p.showPage()
                    y = 750
                date_str = sale.date.strftime('%d-%b-%Y') if sale.date else 'N/A'
                p.drawString(100, y, date_str)
                p.drawString(200, y, str(sale.customer_id)[:30])
                p.drawString(400, y, f"₹{sale.grand_total:,.2f}")
                y -= 15
            
        p.showPage()
        p.save()
        buffer.seek(0)
        return buffer

    @staticmethod
    def generate_stock_valuation_pdf(db: Session):
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        
        # Header
        p.setFillColorRGB(0.13, 0.58, 0.95)
        p.rect(0, 750, 612, 50, fill=1, stroke=0)
        p.setFillColorRGB(1, 1, 1)
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, 770, "STOCK VALUATION REPORT")
        p.setFont("Helvetica", 10)
        p.drawString(100, 755, "Yarn Trading Company")
        
        # Reset color
        p.setFillColorRGB(0, 0, 0)
        p.setFont("Helvetica", 12)
        p.drawString(100, 720, f"Generated on: {datetime.now().strftime('%d %B %Y, %I:%M %p')}")
        
        # Get inventory data
        items = db.query(models.Inventory).all()
        
        # Summary Section
        y = 680
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, y, "INVENTORY SUMMARY")
        p.setFont("Helvetica", 11)
        y -= 25
        total_value = sum(item.total_value or 0 for item in items)
        total_quantity = sum(item.closing_stock or 0 for item in items)
        low_stock_items = [item for item in items if (item.closing_stock or 0) < 50]
        
        p.drawString(120, y, f"Total Inventory Items: {len(items)}")
        y -= 20
        p.drawString(120, y, f"Total Quantity: {total_quantity} units")
        y -= 20
        p.drawString(120, y, f"Total Inventory Value: ₹{total_value:,.2f}")
        y -= 20
        p.drawString(120, y, f"Low Stock Items (< 50 units): {len(low_stock_items)}")
        
        # Low Stock Alert
        if low_stock_items:
            y -= 30
            p.setFont("Helvetica-Bold", 14)
            p.setFillColorRGB(0.8, 0, 0)
            p.drawString(100, y, "⚠ LOW STOCK ALERT")
            p.setFillColorRGB(0, 0, 0)
            p.setFont("Helvetica", 10)
            y -= 20
            for item in low_stock_items[:10]:  # Show top 10 low stock items
                if y < 100:
                    p.showPage()
                    y = 750
                p.drawString(120, y, f"• {item.item_name}: {item.closing_stock} {item.unit or 'units'}")
                y -= 15
        
        # Detailed Inventory List
        y -= 30
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, y, "DETAILED INVENTORY")
        
        # Table Headers
        y -= 25
        p.setFont("Helvetica-Bold", 10)
        p.drawString(50, y, "Item Name")
        p.drawString(180, y, "Category")
        p.drawString(280, y, "Quantity")
        p.drawString(350, y, "Unit Cost")
        p.drawString(430, y, "Total Value")
        p.drawString(520, y, "Status")
        
        y -= 20
        p.setFont("Helvetica", 9)
        
        # Sort by value (highest first)
        sorted_items = sorted(items, key=lambda x: x.total_value or 0, reverse=True)
        
        for item in sorted_items:
            if y < 100:
                p.showPage()
                y = 750
                # Repeat headers on new page
                p.setFont("Helvetica-Bold", 10)
                p.drawString(50, y, "Item Name")
                p.drawString(180, y, "Category")
                p.drawString(280, y, "Quantity")
                p.drawString(350, y, "Unit Cost")
                p.drawString(430, y, "Total Value")
                p.drawString(520, y, "Status")
                y -= 20
                p.setFont("Helvetica", 9)
            
            # Item details
            p.drawString(50, y, str(item.item_name)[:25])
            p.drawString(180, y, str(item.item_category)[:15])
            p.drawString(280, y, f"{item.closing_stock or 0} {item.unit or 'units'}")
            p.drawString(350, y, f"₹{item.unit_cost or 0:,.2f}")
            p.drawString(430, y, f"₹{item.total_value or 0:,.2f}")
            
            # Stock status
            stock_qty = item.closing_stock or 0
            if stock_qty < 20:
                p.setFillColorRGB(0.8, 0, 0)
                p.drawString(520, y, "CRITICAL")
            elif stock_qty < 50:
                p.setFillColorRGB(1, 0.5, 0)
                p.drawString(520, y, "LOW")
            else:
                p.setFillColorRGB(0, 0.5, 0)
                p.drawString(520, y, "OK")
            p.setFillColorRGB(0, 0, 0)
            
            y -= 15
        
        # Category Summary
        y -= 25
        p.setFont("Helvetica-Bold", 12)
        p.drawString(100, y, "CATEGORY SUMMARY")
        p.setFont("Helvetica", 10)
        y -= 20
        
        # Group by category
        category_summary = {}
        for item in items:
            category = item.item_category or 'Uncategorized'
            if category not in category_summary:
                category_summary[category] = {'count': 0, 'value': 0, 'quantity': 0}
            category_summary[category]['count'] += 1
            category_summary[category]['value'] += item.total_value or 0
            category_summary[category]['quantity'] += item.closing_stock or 0
        
        p.drawString(120, y, "Category")
        p.drawString(250, y, "Items")
        p.drawString(320, y, "Quantity")
        p.drawString(400, y, "Value")
        y -= 15
        
        for category, data in sorted(category_summary.items(), key=lambda x: x[1]['value'], reverse=True):
            if y < 100:
                p.showPage()
                y = 750
            p.drawString(120, y, str(category)[:25])
            p.drawString(250, y, str(data['count']))
            p.drawString(320, y, f"{data['quantity']}")
            p.drawString(400, y, f"₹{data['value']:,.2f}")
            y -= 15
        
        p.showPage()
        p.save()
        buffer.seek(0)
        return buffer
    @staticmethod
    def generate_prediction_report_pdf(db: Session, yarn_type: str, prediction: dict, trends: list):
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        
        # Header Theme (Blue accent)
        p.setFillColorRGB(0.13, 0.58, 0.95) # #2196f3
        p.rect(0, 750, 612, 50, fill=1, stroke=0)
        
        p.setFillColorRGB(1, 1, 1)
        p.setFont("Helvetica-Bold", 18)
        p.drawString(40, 770, "AI MARKET ANALYTICS REPORT")
        
        # Metadata
        p.setFillColorRGB(0.2, 0.2, 0.2)
        p.setFont("Helvetica", 10)
        now_str = datetime.now().strftime("%d %b %Y, %H:%M")
        p.drawRightString(570, 755, f"Generated: {now_str}")
        
        # Analysis Overview
        p.setFont("Helvetica-Bold", 14)
        p.drawString(40, 720, f"Commodity: {yarn_type}")
        
        p.setStrokeColorRGB(0.8, 0.8, 0.8)
        p.line(40, 710, 570, 710)
        
        # Prediction Card (Simulated Box)
        p.setFillColorRGB(0.95, 0.97, 1.0)
        p.rect(40, 600, 250, 100, fill=1, stroke=1)
        
        p.setFillColorRGB(0, 0, 0)
        p.setFont("Helvetica", 10)
        p.drawString(50, 680, "FORECASTED RATE")
        p.setFont("Helvetica-Bold", 24)
        p.setFillColorRGB(0.13, 0.58, 0.95)
        p.drawString(50, 650, f"₹{prediction['predicted_price']:,.2f}")
        
        p.setFillColorRGB(0, 0, 0)
        p.setFont("Helvetica", 10)
        p.drawString(50, 630, f"Trend: {prediction['trend']}")
        p.drawString(50, 615, f"Confidence: {prediction['confidence']}")
        
        # History Stats
        p.setFillColorRGB(0.98, 0.98, 0.98)
        p.rect(310, 600, 260, 100, fill=1, stroke=1)
        
        p.setFillColorRGB(0, 0, 0)
        p.setFont("Helvetica", 10)
        p.drawString(320, 680, "HISTORICAL CONTEXT")
        p.setFont("Helvetica-Bold", 12)
        p.drawString(320, 660, f"Historical Avg: ₹{prediction.get('historical_avg', 0):,.2f}")
        p.setFont("Helvetica", 10)
        p.drawString(320, 640, f"Analysis Points: {prediction['history_count']} purchases")
        p.drawString(320, 620, f"Data Range: Last 12 months (est)")
        
        # Trend Table Header
        y = 550
        p.setFont("Helvetica-Bold", 12)
        p.drawString(40, y, "Price Trend & Projections")
        y -= 25
        
        p.setFillColorRGB(0.9, 0.9, 0.9)
        p.rect(40, y, 530, 20, fill=1, stroke=0)
        p.setFillColorRGB(0, 0, 0)
        p.setFont("Helvetica-Bold", 10)
        p.drawString(50, y+5, "Month")
        p.drawString(200, y+5, "Average Rate (₹)")
        p.drawString(400, y+5, "Type")
        y -= 20
        
        # Trend Rows
        p.setFont("Helvetica", 10)
        
        # Add historical trends
        for point in trends[-5:]: # Last 5 historical points
            if y < 100:
                p.showPage()
                y = 750
            
            p.drawString(50, y, point['month'])
            p.drawString(200, y, f"₹{point['rate']:,.2f}")
            p.drawString(400, y, "Actual Market")
            
            p.setStrokeColorRGB(0.9, 0.9, 0.9)
            p.line(40, y-5, 570, y-5)
            y -= 20
        
        # Add 3-month predictions
        if prediction.get('three_month_prediction'):
            p.setFont("Helvetica-Bold", 10)
            p.drawString(50, y, "--- FUTURE PREDICTIONS ---")
            y -= 20
            
            for month_pred in prediction['three_month_prediction']:
                if y < 100:
                    p.showPage()
                    y = 750
                
                p.drawString(50, y, month_pred['month'])
                p.drawString(200, y, f"₹{month_pred['predicted_price']:,.2f}")
                p.drawString(400, y, "AI Projection")
                
                p.setStrokeColorRGB(0.9, 0.9, 0.9)
                p.line(40, y-5, 570, y-5)
                y -= 20
            
        # Footer
        p.setFont("Helvetica-Oblique", 8)
        p.setFillColorRGB(0.5, 0.5, 0.5)
        p.drawString(40, 50, "Disclaimer: AI predictions are based on historical data and may not account for sudden black-swan market shifts.")
        p.drawRightString(570, 50, "Yarn Trading Accountancy Platform")
        
        p.showPage()
        p.save()
        buffer.seek(0)
        return buffer
from datetime import datetime
