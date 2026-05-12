# fix_group_form.py
html = '''<!DOCTYPE html>
<html lang="sw">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fomu ya Mkopo wa Kikundi - Orethan Microfinance</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: #f0f0f0; padding: 20px; }
        .form-container { max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
        .header { text-align: center; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 2px solid #2c5aa6; }
        .company-name { font-size: 22px; font-weight: bold; color: #2c5aa6; }
        .company-address { font-size: 11px; color: #666; margin-top: 5px; }
        .section { margin-bottom: 30px; padding: 15px; background: #f9f9f9; border-radius: 8px; }
        .section-title { font-size: 18px; font-weight: bold; margin-bottom: 15px; padding-bottom: 8px; border-bottom: 2px solid #2c5aa6; color: #2c5aa6; }
        .form-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; }
        .form-field { margin-bottom: 10px; }
        .form-field label { display: block; font-weight: bold; margin-bottom: 5px; font-size: 13px; }
        .form-field input, .form-field select, .form-field textarea { width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; }
        .full-width { grid-column: span 2; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background: #2c5aa6; color: white; }
        .btn-add { background: #28a745; color: white; padding: 5px 15px; border: none; cursor: pointer; margin-top: 10px; }
        .declaration { margin: 15px 0; padding: 15px; background: #fff3cd; border-left: 4px solid #ffc107; }
        .signature-area { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 20px; }
        .signature-line { border-top: 1px solid #333; margin-top: 30px; padding-top: 10px; }
        .btn-submit { background: #2c5aa6; color: white; padding: 12px 30px; border: none; border-radius: 5px; cursor: pointer; width: 100%; font-size: 16px; }
        .btn-back { background: #6c757d; color: white; padding: 8px 20px; border: none; border-radius: 5px; cursor: pointer; margin-bottom: 20px; text-decoration: none; display: inline-block; }
        @media (max-width: 768px) { .form-grid { grid-template-columns: 1fr; } .full-width { grid-column: span 1; } }
    </style>
</head>
<body>
    <div class="form-container">
        <a href="/client_dashboard" class="btn-back">← Nyuma</a>
        <div class="header">
            <div class="company-name">ORETHAN MICROFINANCE</div>
            <div class="company-address">Mbagala, Zakhien - Ground, P.O Box 77286.<br>Dar es Salaam, Tanzania.<br>(+255) 769 337 774</div>
        </div>
        <h2 style="text-align:center; margin-bottom:20px;">FOMU YA MAOMBI YA MKOPO WA KIKUNDI</h2>
        <form method="POST" action="/submit_group_loan">
            <!-- SECTION 1 -->
            <div class="section">
                <div class="section-title">1. TAARIFA ZA MWOMBAJI</div>
                <div class="form-grid">
                    <div class="form-field"><label>Jina kamili</label><input type="text" name="applicant_full_name" required></div>
                    <div class="form-field"><label>Jinsia</label><select name="gender"><option>Me</option><option>Ke</option></select></div>
                    <div class="form-field"><label>Jina maarufu</label><input type="text" name="applicant_known_name"></div>
                    <div class="form-field"><label>Aina ya Kitambulisho</label><input type="text" name="id_type"></div>
                    <div class="form-field"><label>Namba ya Kitambulisho</label><input type="text" name="id_number"></div>
                    <div class="form-field"><label>Tarehe ya kuzaliwa</label><input type="date" name="birth_date"></div>
                    <div class="form-field"><label>Simu</label><input type="tel" name="phone"></div>
                    <div class="form-field"><label>Hali ya Ndoa</label><select name="marital_status"><option>Hajaoa/Olewa</option><option>Ameo/Olewa</option></select></div>
                    <div class="form-field full-width"><label>Eneo unaloshini</label><input type="text" name="residence_area"></div>
                    <div class="form-field"><label>Umeishi tangu lini</label><input type="text" name="residence_since"></div>
                    <div class="form-field"><label>Uniliki wa Makazi</label><select name="residence_ownership"><option>Kwako</option><option>Umepanga</option></select></div>
                    <div class="form-field"><label>Jina la mume/mke</label><input type="text" name="spouse_full_name"></div>
                    <div class="form-field"><label>Jina maarufu</label><input type="text" name="spouse_known_name"></div>
                    <div class="form-field"><label>Tarehe ya kuzaliwa</label><input type="date" name="spouse_birth_date"></div>
                    <div class="form-field"><label>Idadi ya utegemezi</label><input type="number" name="dependents_count"></div>
                    <div class="form-field"><label>Simu</label><input type="tel" name="spouse_phone"></div>
                </div>
            </div>
            <!-- SECTION 2 -->
            <div class="section">
                <div class="section-title">2. TAARIFA ZA KIKUNDI</div>
                <div class="form-grid">
                    <div class="form-field"><label>Jina la Mwenyekiti</label><input type="text" name="group_chairperson"></div>
                    <div class="form-field"><label>Jina la Katibu</label><input type="text" name="group_secretary"></div>
                    <div class="form-field full-width"><label>Anuani ya Kikundi</label><input type="text" name="group_address"></div>
                    <div class="form-field"><label>Namba ya usajili</label><input type="text" name="group_reg_number"></div>
                    <div class="form-field"><label>Mkoa</label><input type="text" name="region"></div>
                    <div class="form-field"><label>Wilaya</label><input type="text" name="district"></div>
                    <div class="form-field"><label>Kata</label><input type="text" name="ward"></div>
                    <div class="form-field"><label>Kijiji/mtaa</label><input type="text" name="village"></div>
                    <div class="form-field"><label>Wanachama (ME)</label><input type="number" name="male_members"></div>
                    <div class="form-field"><label>Wanachama (KE)</label><input type="number" name="female_members"></div>
                    <div class="form-field"><label>Tarehe ya usajili</label><input type="date" name="registration_date"></div>
                    <div class="form-field"><label>Simu 1</label><input type="tel" name="group_phone1"></div>
                    <div class="form-field"><label>Simu 2</label><input type="tel" name="group_phone2"></div>
                </div>
            </div>
            <!-- SECTION 3 -->
            <div class="section">
                <div class="section-title">3. TAARIFA ZA MIRADI</div>
                <div class="form-grid">
                    <div class="form-field"><label>Jina la Mradi</label><input type="text" name="project_name"></div>
                    <div class="form-field"><label>Aina ya Mradi</label><input type="text" name="project_type"></div>
                    <div class="form-field full-width"><label>Mahali Mradi upo</label><input type="text" name="project_location"></div>
                    <div class="form-field"><label>Kata</label><input type="text" name="project_ward"></div>
                    <div class="form-field"><label>Wilaya</label><input type="text" name="project_district"></div>
                    <div class="form-field"><label>Mradi umeanza lini</label><input type="date" name="project_start_date"></div>
                    <div class="form-field"><label>Kipato kwa mwezi (Tsh)</label><input type="number" name="monthly_income"></div>
                    <div class="form-field"><label>Matumizi kwa mwezi (Tsh)</label><input type="number" name="monthly_expenses"></div>
                </div>
            </div>
            <!-- SECTION 4 -->
            <div class="section">
                <div class="section-title">4. KIASI CHA MKOPO</div>
                <div class="form-grid">
                    <div class="form-field"><label>Kiasi cha Mkopo (Tsh)</label><input type="number" name="loan_amount" required></div>
                    <div class="form-field"><label>Muda wa kulipa (miezi)</label><input type="number" name="repayment_period"></div>
                    <div class="form-field full-width"><label>Kiasi cha rejesho kwa mwezi</label><input type="number" name="affordable_repayment"></div>
                    <div class="form-field full-width"><label>Malengo ya Mkopo</label><textarea name="loan_purpose" rows="3"></textarea></div>
                    <div class="form-field"><label>Deni la kikundi</label><input type="number" name="group_existing_debt"></div>
                    <div class="form-field"><label>Kikundi kimewahi kukopa?</label><select name="previous_loan"><option>HAPANA</option><option>NDIVO</option></select></div>
                    <div class="form-field full-width"><label>Chanzo cha mapato</label><input type="text" name="income_source"></div>
                </div>
            </div>
            <!-- SECTION 5 -->
            <div class="section">
                <div class="section-title">5. MDHAMINI NO. 1 (MWENYEKITI)</div>
                <div class="form-grid">
                    <div class="form-field"><label>Jina kamili</label><input type="text" name="guarantor1_full_name"></div>
                    <div class="form-field"><label>Mahali anapoishi</label><input type="text" name="guarantor1_residence"></div>
                    <div class="form-field"><label>Namba ya nyumba</label><input type="text" name="guarantor1_house_number"></div>
                    <div class="form-field"><label>Amepanga/Kwake</label><input type="text" name="guarantor1_rent_status"></div>
                    <div class="form-field"><label>Kazi anayofanya</label><input type="text" name="guarantor1_occupation"></div>
                    <div class="form-field"><label>Mahali ilipo ofisi</label><input type="text" name="guarantor1_office_location"></div>
                    <div class="form-field"><label>Jina la kampuni</label><input type="text" name="guarantor1_company"></div>
                    <div class="form-field"><label>Simu</label><input type="tel" name="guarantor1_phone"></div>
                </div>
            </div>
            <!-- SECTION 6 -->
            <div class="section">
                <div class="section-title">6. MDHAMINI NO. 2 (MUME/MKE/NDUGU)</div>
                <div class="form-grid">
                    <div class="form-field"><label>Jina kamili</label><input type="text" name="guarantor2_full_name"></div>
                    <div class="form-field"><label>Uhusiano</label><input type="text" name="guarantor2_relationship"></div>
                    <div class="form-field"><label>Mahali anapoishi</label><input type="text" name="guarantor2_residence"></div>
                    <div class="form-field"><label>Namba ya nyumba</label><input type="text" name="guarantor2_house_number"></div>
                    <div class="form-field"><label>Amepanga/Kwake</label><input type="text" name="guarantor2_rent_status"></div>
                    <div class="form-field"><label>Kazi anayofanya</label><input type="text" name="guarantor2_occupation"></div>
                    <div class="form-field"><label>Mahali ilipo ofisi</label><input type="text" name="guarantor2_office_location"></div>
                    <div class="form-field"><label>Jina la kampuni</label><input type="text" name="guarantor2_company"></div>
                    <div class="form-field"><label>Simu</label><input type="tel" name="guarantor2_phone"></div>
                </div>
            </div>
            <!-- SECTION 7: DHAMANA -->
            <div class="section">
                <div class="section-title">7. TAARIFA ZA DHAMANA</div>
                <div class="form-field"><label>Aina ya Dhamana</label><input type="text" name="collateral_type"></div>
                <div class="form-field"><label>Namba ya usajili</label><input type="text" name="collateral_reg_no"></div>
                <div class="form-field"><label>Thamani ya dhamana (Tsh)</label><input type="number" name="collateral_value"></div>
                <div class="form-field"><label>Mahali Ilipo</label><input type="text" name="collateral_location"></div>
            </div>
            <!-- TAMKO -->
            <div class="section">
                <div class="section-title">8. TAMKO LA MWOMBAJI</div>
                <div class="declaration">
                    <p>Mimi <input type="text" name="applicant_declaration_name" placeholder="Jina lako" style="width:200px"> nimeomba mkopo wa Tsh <input type="text" name="applicant_declaration_amount" placeholder="Kiasi" style="width:150px"> kutoka Orethan Microfinance. Nakiri kwamba taarifa zote nilizozitoa hapo juu ni sahihi.</p>
                </div>
                <div class="signature-area">
                    <div><div class="signature-line">SAHIHI</div><input type="text" name="applicant_signature" placeholder="Sahihi"></div>
                    <div><div class="signature-line">TAREHE</div><input type="date" name="applicant_date"></div>
                    <div><div class="signature-line">DOLE GUMBA</div><input type="text" name="applicant_thumbprint" placeholder="Alama ya gumba"></div>
                </div>
            </div>
            <button type="submit" class="btn-submit">WASILISHA MAOMBI</button>
        </form>
    </div>
</body>
</html>'''

with open('templates/group_loan_form.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("✅ group_loan_form.html has been fixed!")
