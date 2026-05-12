# troubleshoot_group_form.py
import os

# Check if the form file exists and verify its content
form_path = 'templates/group_loan_form.html'
if os.path.exists(form_path):
    with open(form_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for key features of the new form
    checks = {
        'Multi-page indicators': 'page-indicator' in content,
        '6 pages navigation': 'showPage(6)' in content,
        'Navigation buttons': 'NEXT →' in content,
        'Table on page 5': 'TAARIFA ZA DHAMANA' in content,
        'JavaScript functionality': 'function showPage' in content,
        'Form sections': 'page1 class="page active"' in content
    }
    
    print("🔍 GROUP LOAN FORM VERIFICATION:")
    print("=" * 50)
    for feature, exists in checks.items():
        status = "✅" if exists else "❌"
        print(f"{status} {feature}: {'Found' if exists else 'Missing'}")
    
    print("\n📋 FILE SIZE:", len(content), "characters")
    print("📄 LINES:", content.count('\n'), "lines")
    
    if all(checks.values()):
        print("\n🎉 NEW MULTI-PAGE FORM IS CORRECTLY INSTALLED!")
        print("\n🔧 TROUBLESHOOTING STEPS:")
        print("1. Clear browser cache (Ctrl+F5 or Cmd+Shift+R)")
        print("2. Try a different browser")
        print("3. Check you're accessing the correct route:")
        print("   - /group_loan_form")
        print("   - /apply_group_loan")
        print("4. Make sure server restarted successfully")
    else:
        print("\n⚠️ Some features are missing - form may not be complete")
else:
    print("❌ Form file not found at:", form_path)
