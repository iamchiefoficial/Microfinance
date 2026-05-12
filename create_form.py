# create_form.py
import os

# Make sure templates directory exists
os.makedirs("templates", exist_ok=True)

html_content = """<!DOCTYPE html>
<html lang="sw">
<head>
    <meta charset="UTF-8">
    <title>Fomu ya Mkopo wa Kikundi - Orethan Microfinance</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:Arial;background:#f0f0f0;padding:20px}
        .container{max-width:900px;margin:0 auto;background:white;padding:30px;border-radius:10px}
        .header{text-align:center;margin-bottom:30px;padding-bottom:20px;border-bottom:2px solid #2c5aa6}
        .company-name{font-size:24px;font-weight:bold;color:#2c5aa6}
        .company-address{font-size:12px;color:#666}
        .section{margin-bottom:25px;padding:15px;background:#f9f9f9;border-radius:8px}
        .section-title{font-size:18px;font-weight:bold;margin-bottom:15px;padding-bottom:8px;border-bottom:2px solid #2c5aa6;color:#2c5aa6}
        .form-row{display:flex;gap:15px;margin-bottom:12px;flex-wrap:wrap}
        .form-field{flex:1;min-width:200px}
        .form-field label{display:block;font-weight:bold;margin-bottom:5px;font-size:13px}
        .form-field input,.form-field select,.form-field textarea{width:100%;padding:8px;border:1px solid #ccc;border-radius:4px}
        .full-width{width:100%}
        .btn-submit{background:#2c5aa6;color:white;padding:12px 30px;border:none;border-radius:5px;cursor:pointer;width:100%;font-size:16px;margin-top:20px}
        .btn-back{background:#6c757d;color:white;padding:8px 20px;border:none;border-radius:5px;cursor:pointer;margin-bottom:20px;text-decoration:none;display:inline-block}
        h2{text-align:center;margin:20px 0;color:#2c5aa6}
    </style>
</head>
<body>
<div class="container">
    <a href="/client_dashboard" class="btn-back">← Nyuma</a>
    <div class="header">
        <div class="company-name">ORETHAN MICROFINANCE</div>
        <div class="company-address">Mbagala, Zakhien - Ground | (+255) 769 337 774</div>
    </div>
    <h2>FOMU YA MAOMBI YA MKOPO WA KIKUNDI</h2>
    
    <form method="POST" action="/submit_group_loan">
        <!-- Sehemu ya 1 -->
        <div class="section">
            <div class="section-title">1. TAARIFA ZA MWOMBAJI</div>
            <div class="form-row">
                <div class="form-field"><label>Jina kamili *</label><input type="text" name="applicant_full_name" required></div>
                <div class="form-field"><label>Jinsia</label><select name="gender"><option>Me</option><option>Ke</option></select></div>
            </div>
            <div class="form-row">
                <div class="form-field"><label>Jina maarufu</label><input type="text" name="applicant_known_name"></div>
                <div class="form-field"><label>Aina ya Kitambulisho</label><input type="text" name="id_type"></div>
            </div>
            <div class="form-row">
                <div class="form-field"><label>Namba ya Kitambulisho</label><input type="text" name="id_number"></div>
                <div class="form-field"><label>Tarehe ya kuzaliwa</label><input type="date" name="birth_date"></div>
            </div>
            <div class="form-row">
                <div class="form-field"><label>Simu</label><input type="tel" name="phone"></div>
                <div class="form-field"><label>Hali ya Ndoa</label><select name="marital_status"><option>Hajaoa/Olewa</option><option>Ameo/Olewa</option><option>Ameachika</option><option>Mjane</option></select></div>
            </div>
            <div class="form-row">
                <div class="form-field"><label>Eneo unaloshini</label><input type="text" name="residence_area"></div>
                <div class="form-field"><label>Umeishi tangu lini</label><input type="text" name="residence_since"></div>
            </div>
            <div class="form-row">
                <div class="form-field"><label>Uniliki wa Makazi</label><select name="residence_ownership"><option>Kwako</option><option>Umepanga</option></select></div>
                <div class="form-field"><label>Jina la mume/mke</label><input type="text" name="spouse_full_name"></div>
            </div>
            <div class="form-row">
                <div class="form-field"><label>Idadi ya utegemezi</label><input type="number" name="dependents_count"></div>
                <div class="form-field"><label>Simu ya mwenzi</label><input type="tel" name="spouse_phone"></div>
            </div>
        </div>
        
        <!-- Sehemu ya 2 -->
        <div class="section">
            <div class="section-title">2. TAARIFA ZA KIKUNDI</div>
            <div class="form-row">
                <div class="form-field"><label>Jina la Mwenyekiti</label><input type="text" name="group_chairperson"></div>
                <div class="form-field"><label>Jina la Katibu</label><input type="text" name="group_secretary"></div>
            </div>
            <div class="form-row">
                <div class="form-field full-width"><label>Anuani ya Kikundi</label><input type="text" name="group_address"></div>
            </div>
            <div class="form-row">
                <div class="form-field"><label>Namba ya usajili</label><input type="text" name="group_reg_number"></div>
                <div class="form-field"><label>Tarehe ya usajili</label><input type="date" name="registration_date"></div>
            </div>
            <div class="form-row">
                <div class="form-field"><label>Mkoa</label><input type="text" name="region"></div>
                <div class="form-field"><label>Wilaya</label><input type="text" name="district"></div>
            </div>
            <div class="form-row">
                <div class="form-field"><label>Kata</label><input type="text" name="ward"></div>
                <div class="form-field"><label>Kijiji/mtaa</label><input type="text" name="village"></div>
            </div>
            <div class="form-row">
                <div class="form-field"><label>Wanachama (Wanaume)</label><input type="number" name="male_members"></div>
                <div class="form-field"><label>Wanachama (Wanawake)</label><input type="number" name="female_members"></div>
            </div>
            <div class="form-row">
                <div class="form-field"><label>Simu 1</label><input type="tel" name="group_phone1"></div>
                <div class="form-field"><label>Simu 2</label><input type="tel" name="group_phone2"></div>
            </div>
        </div>
        
        <!-- Sehemu ya 3 -->
        <div class="section">
            <div class="section-title">3. TAARIFA ZA MIRADI</div>
            <div class="form-row">
                <div class="form-field"><label>Jina la Mradi</label><input type="text" name="project_name"></div>
                <div class="form-field"><label>Aina ya Mradi</label><input type="text" name="project_type"></div>
            </div>
            <div class="form-row">
                <div class="form-field full-width"><label>Mahali Mradi upo</label><input type="text" name="project_location"></div>
            </div>
            <div class="form-row">
                <div class="form-field"><label>Kata</label><input type="text" name="project_ward"></div>
                <div class="form-field"><label>Wilaya</label><input type="text" name="project_district"></div>
            </div>
            <div class="form-row">
                <div class="form-field"><label>Mradi umeanza lini</label><input type="date" name="project_start_date"></div>
                <div class="form-field"><label>Kipato kwa mwezi (Tsh)</label><input type="number" name="monthly_income"></div>
            </div>
            <div class="form-row">
                <div class="form-field"><label>Matumizi kwa mwezi (Tsh)</label><input type="number" name="monthly_expenses"></div>
            </div>
        </div>
        
        <!-- Sehemu ya 4 -->
        <div class="section">
            <div class="section-title">4. KIASI CHA MKOPO</div>
            <div class="form-row">
                <div class="form-field"><label>Kiasi cha Mkopo (Tsh) *</label><input type="number" name="loan_amount" required></div>
                <div class="form-field"><label>Muda wa kulipa (miezi)</label><input type="number" name="repayment_period"></div>
            </div>
            <div class="form-row">
                <div class="form-field"><label>Kiasi cha rejesho kwa mwezi (Tsh)</label><input type="number" name="affordable_repayment"></div>
                <div class="form-field"><label>Kikundi kimewahi kukopa?</label><select name="previous_loan"><option>HAPANA</option><option>NDIVO</option></select></div>
            </div>
            <div class="form-row">
                <div class="form-field full-width"><label>Malengo ya Mkopo</label><textarea name="loan_purpose" rows="3"></textarea></div>
            </div>
            <div class="form-row">
                <div class="form-field"><label>Deni la kikundi (Tsh)</label><input type="number" name="group_existing_debt"></div>
                <div class="form-field"><label>Chanzo cha mapato</label><input type="text" name="income_source"></div>
            </div>
        </div>
        
        <!-- Sehemu ya 5 -->
        <div class="section">
            <div class="section-title">5. MDHAMINI NO.1 (MWENYEKITI)</div>
            <div class="form-row">
                <div class="form-field"><label>Jina kamili</label><input type="text" name="guarantor1_full_name"></div>
                <div class="form-field"><label>Mahali anapoishi</label><input type="text" name="guarantor1_residence"></div>
            </div>
            <div class="form-row">
                <div class="form-field"><label>Kazi anayofanya</label><input type="text" name="guarantor1_occupation"></div>
                <div class="form-field"><label>Simu</label><input type="tel" name="guarantor1_phone"></div>
            </div>
        </div>
        
        <!-- Sehemu ya 6 -->
        <div class="section">
            <div class="section-title">6. MDHAMINI NO.2 (MUME/MKE/NDUGU)</div>
            <div class="form-row">
                <div class="form-field"><label>Jina kamili</label><input type="text" name="guarantor2_full_name"></div>
                <div class="form-field"><label>Uhusiano</label><input type="text" name="guarantor2_relationship"></div>
            </div>
            <div class="form-row">
                <div class="form-field"><label>Mahali anapoishi</label><input type="text" name="guarantor2_residence"></div>
                <div class="form-field"><label>Simu</label><input type="tel" name="guarantor2_phone"></div>
            </div>
        </div>
        
        <!-- Sehemu ya 7 -->
        <div class="section">
            <div class="section-title">7. DHAMANA</div>
            <div class="form-row">
                <div class="form-field"><label>Aina ya Dhamana</label><input type="text" name="collateral_type"></div>
                <div class="form-field"><label>Thamani (Tsh)</label><input type="number" name="collateral_value"></div>
            </div>
        </div>
        
        <button type="submit" class="btn-submit">WASILISHA MAOMBI</button>
    </form>
</div>
</body>
</html>"""

# Write the file
with open("templates/group_loan_form.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ group_loan_form.html created successfully!")
print("📁 File location: templates/group_loan_form.html")
print("📏 File size:", len(html_content), "characters")
