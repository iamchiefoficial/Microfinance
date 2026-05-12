# PowerShell script to add approved_by column
Write-Host "Adding approved_by column to loans table..."

try {
    $result = mysql -u root -p microfinance_db -e "ALTER TABLE loans ADD COLUMN approved_by VARCHAR(100) DEFAULT NULL;"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Database column added successfully!"
    } else {
        Write-Host "❌ Error adding column: $LASTEXITCODE"
    }
    
    Write-Host "Operation completed. Press any key to continue..."
    $null = $Host.UI.RawUI.ReadKey()
} catch {
    Write-Host "❌ PowerShell error: $_"
    Write-Host "Operation completed. Press any key to continue..."
    $null = $Host.UI.RawUI.ReadKey()
}
