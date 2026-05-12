# replace_group_loan_form.py
import os

# Delete old form files if they exist
old_files = ['templates/group_loan_form.html', 'templates/group_loan_form_new.html']
for file_path in old_files:
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f'✅ Deleted old file: {file_path}')
    except:
        print(f'⚠️ Could not delete: {file_path}')

# Create NEW complete multi-page group loan form
content = '''<!DOCTYPE html>
<html lang="sw">
<head>
    <meta charset="UTF-8">
    <title>Fomu ya Mkopo wa Kikundi - Orethan Microfinance</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:'Times New Roman',Arial;background:#e0e0e0;padding:20px}
        .form-container{max-width:1100px;margin:0 auto;background:white;padding:25px;border-radius:10px;box-shadow:0 0 20px rgba(0,0,0,0.2)}
        .header{text-align:center;margin-bottom:20px;padding-bottom:15px;border-bottom:2px solid #2c5aa6}
        .company-name{font-size:24px;font-weight:bold;color:#2c5aa6}
        .company-address{font-size:11px;color:#666}
        .form-no{text-align:right;margin-bottom:10px;font-size:12px;font-weight:bold}
        h2{text-align:center;margin:15px 0;color:#2c5aa6;font-size:20px}
        .page{display:none;animation:fadeIn 0.5s}
        .page.active{display:block}
        @keyframes fadeIn{from{opacity:0;}to{opacity:1;}}
        .section{background:#f9f9f9;padding:20px;margin-bottom:20px;border-radius:8px;border:1px solid #ddd}
        .section-title{font-size:16px;font-weight:bold;margin-bottom:15px;padding-bottom:8px;border-bottom:2px solid #2c5aa6;color:#2c5aa6}
        .form-row{display:flex;gap:15px;margin-bottom:12px;flex-wrap:wrap}
        .form-field{flex:1;min-width:180px}
        .form-field label{display:block;font-weight:bold;margin-bottom:5px;font-size:11px}
        .form-field input,.form-field select,.form-field textarea{width:100%;padding:6px;border:1px solid #ccc;border-radius:4px;font-size:12px}
        .radio-group{display:flex;gap:15px;margin-top:5px;flex-wrap:wrap}
        .radio-group label{display:inline-flex;align-items:center;gap:5px;font-weight:normal;font-size:12px}
        table{width:100%;border-collapse:collapse;margin-top:10px;font-size:11px}
        th,td{border:1px solid #ddd;padding:6px;text-align:left}
        th{background:#2c5aa6;color:white;font-size:11px}
        .btn-add{background:#28a745;color:white;padding:5px 15px;border:none;border-radius:4px;cursor:pointer;margin-top:10px;font-size:12px}
        .btn-remove{background:#dc3545;color:white;padding:2px 8px;border:none;border-radius:3px;cursor:pointer;font-size:10px}
        .nav-buttons{display:flex;justify-content:space-between;margin-top:30px;padding-top:20px;border-top:1px solid #ddd}
        .btn-nav{background:#2c5aa6;color:white;padding:10px 25px;border:none;border-radius:5px;cursor:pointer;font-size:14px}
        .btn-nav:hover{background:#1e3d6e}
        .btn-submit{background:#28a745}
        .page-indicator{text-align:center;margin-bottom:20px;font-size:14px;color:#666}
        .page-btn{display:inline-block;width:32px;height:32px;line-height:32px;text-align:center;border-radius:50%;background:#ddd;margin:0 5px;cursor:pointer;font-size:12px}
        .page-btn.active{background:#2c5aa6;color:white}
        .declaration{background:#fff3cd;padding:12px;border-left:4px solid #ffc107;margin:15px 0;font-size:12px}
        .signature-area{display:grid;grid-template-columns:repeat(3,1fr);gap:15px;margin-top:15px}
        .signature-line{border-top:1px solid #000;margin-top:25px;padding-top:8px;text-align:center;font-size:11px}
        @media print{.nav-buttons,.page-indicator{display:none}.page{display:block!important}}
    </style>
</head>
<body>
<div class="form-container">
    <div class="form-no">Fomu No: ______________</div>
    <div class="header">
        <div class="company-name">🏦 ORETHAN MICROFINANCE</div>
        <div class="company-address">Mbagala, Zakhiem- Ground, P.O Box 77286.<br>Dar es Salaam, Tanzania.<br>(+255) 769 337 774 / (+255) 702 519 104<br>orethantanzanialimited@gmail.com</div>
    </div>
    <h2>FOMU YA MAOMBI YA MKOPO WA KIKUNDI</h2>
    
    <div class="page-indicator">
        <span class="page-btn active" onclick="showPage(1)">1</span>
        <span class="page-btn" onclick="showPage(2)">2</span>
        <span class="page-btn" onclick="showPage(3)">3</span>
        <span class="page-btn" onclick="showPage(4)">4</span>
        <span class="page-btn" onclick="showPage(5)">5</span>
        <span class="page-btn" onclick="showPage(6)">6</span>
    </div>
    
    <form method="POST" action="/submit_group_loan" id="groupLoanForm">
        <!-- PAGE 1: TAARIFA ZA MWOMBAJI -->
        <div id="page1" class="page active">
            <div class="section">
                <div class="section-title">1. TAARIFA ZA MWOMBAJI</div>
                <div class="form-row">
                    <div class="form-field"><label>Jina kamili la mwombaji</label><input type="text" name="applicant_full_name" required></div>
                    <div class="form-field"><label>Jinsia</label><select name="gender"><option>Me</option><option>Ke</option></select></div>
                </div>
                <div class="form-row">
                    <div class="form-field"><label>Jina maarufu</label><input type="text" name="applicant_known_name"></div>
                    <div class="form-field"><label>Aina ya Kitambulisho</label><input type="text" name="id_type"></div>
                </div>
                <div class="form-row">
                    <div class="form-field"><label>Namba ya Kitambulisho</label><input type="text" name="id_number"></div>
                </div>
                <div class="form-row">
                    <div class="form-field"><label>Tarehe ya kuzaliwa</label><input type="date" name="birth_date"></div>
                    <div class="form-field"><label>Simu</label><input type="tel" name="phone"></div>
                </div>
                <div class="form-row">
                    <div class="form-field"><label>Hali ya Ndoa</label>
                        <div class="radio-group">
                            <label><input type="radio" name="marital_status" value="Hajaoa/Olewa"> Hajaoa/Olewa</label>
                            <label><input type="radio" name="marital_status" value="Ameoa/Olewa"> Ameoa/Olewa</label>
                            <label><input type="radio" name="marital_status" value="Ameachika"> Ameachika</label>
                            <label><input type="radio" name="marital_status" value="Mjane/Mgane"> Mjane/Mgane</label>
                        </div>
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-field"><label>Eneo unaloishi</label><input type="text" name="residence_area"></div>
                    <div class="form-field"><label>Umeishi hapo tangu lini</label><input type="text" name="residence_since"></div>
                </div>
                <div class="form-row">
                    <div class="form-field"><label>Umiliki wa Makazi</label>
                        <div class="radio-group">
                            <label><input type="radio" name="residence_ownership" value="Kwako"> Kwako</label>
                            <label><input type="radio" name="residence_ownership" value="Umepanga"> Umepanga</label>
                            <label><input type="radio" name="residence_ownership" value="Mengine"> Mengine</label>
                        </div>
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-field"><label>Jina kamili la mume/mke</label><input type="text" name="spouse_full_name"></div>
                    <div class="form-field"><label>Jina maarufu mtaani</label><input type="text" name="spouse_known_name"></div>
                </div>
                <div class="form-row">
                    <div class="form-field"><label>Tarehe ya kuzaliwa</label><input type="date" name="spouse_birth_date"></div>
                    <div class="form-field"><label>Idadi ya utegemezi</label><input type="number" name="dependents_count"></div>
                    <div class="form-field"><label>Simu</label><input type="tel" name="spouse_phone"></div>
                </div>
            </div>
        </div>
        
        <!-- PAGE 2: TAARIFA ZA KIKUNDI + TAARIFA ZA MIRADI -->
        <div id="page2" class="page">
            <div class="section">
                <div class="section-title">2. TAARIFA ZA KIKUNDI</div>
                <div class="form-row">
                    <div class="form-field"><label>Jina la Mwenyekiti</label><input type="text" name="group_chairperson"></div>
                    <div class="form-field"><label>Jina la Katibu</label><input type="text" name="group_secretary"></div>
                </div>
                <div class="form-row">
                    <div class="form-field"><label>Anuani ya Makazi ya kikundi</label><input type="text" name="group_address"></div>
                    <div class="form-field"><label>Namba ya usajili wa kikundi</label><input type="text" name="group_reg_number"></div>
                </div>
                <div class="form-row">
                    <div class="form-field"><label>Mkoa</label><input type="text" name="region"></div>
                    <div class="form-field"><label>Wilaya</label><input type="text" name="district"></div>
                    <div class="form-field"><label>Kata</label><input type="text" name="ward"></div>
                    <div class="form-field"><label>Kijiji/mtaa</label><input type="text" name="village"></div>
                </div>
                <div class="form-row">
                    <div class="form-field"><label>Idadi ya wanachama (ME)</label><input type="number" name="male_members"></div>
                    <div class="form-field"><label>Idadi ya wanachama (KE)</label><input type="number" name="female_members"></div>
                </div>
                <div class="form-row">
                    <div class="form-field"><label>Tarehe ya usajiri</label><input type="date" name="registration_date"></div>
                    <div class="form-field"><label>Simu 1</label><input type="tel" name="group_phone1"></div>
                    <div class="form-field"><label>Simu 2</label><input type="tel" name="group_phone2"></div>
                </div>
            </div>
            
            <div class="section">
                <div class="section-title">3. TAARIFA ZA MIRADI</div>
                <div class="form-row">
                    <div class="form-field"><label>Jina la Mradi</label><input type="text" name="project_name"></div>
                    <div class="form-field"><label>Aina ya Mradi</label><input type="text" name="project_type"></div>
                </div>
                <div class="form-row">
                    <div class="form-field"><label>Mahali mradi upo</label><input type="text" name="project_location"></div>
                    <div class="form-field"><label>Kata</label><input type="text" name="project_ward"></div>
                    <div class="form-field"><label>Wilaya</label><input type="text" name="project_district"></div>
                </div>
                <div class="form-row">
                    <div class="form-field"><label>Wastani wa kipato kwa mwezi (Tsh)</label><input type="number" name="monthly_income"></div>
                    <div class="form-field"><label>Wastani wa matumizi kwa mwezi (Tsh)</label><input type="number" name="monthly_expenses"></div>
                </div>
                <div class="form-row">
                    <div class="form-field"><label>Mradi umeanza lini</label><input type="date" name="project_start_date"></div>
                </div>
            </div>
        </div>
        
        <!-- PAGE 3: KIASI CHA MKOPO -->
        <div id="page3" class="page">
            <div class="section">
                <div class="section-title">4. KIASI CHA MKOPO KINACHOOMBWA</div>
                <div class="form-row">
                    <div class="form-field"><label>Kiasi cha Mkopo (Tsh)</label><input type="number" name="loan_amount" required></div>
                    <div class="form-field"><label>Muda wa kulipa Mkopo (miezi)</label><input type="number" name="repayment_period"></div>
                </div>
                <div class="form-row">
                    <div class="form-field"><label>Ni kiasi gani cha rejesho unaweza kulipa bila matatizo (Tsh)</label><input type="number" name="affordable_repayment"></div>
                </div>
                <div class="form-row">
                    <div class="form-field"><label>Malengo ya Mkopo</label><textarea name="loan_purpose" rows="3"></textarea></div>
                    <div class="form-field"><label>Kiasi kikundi kinadaiwa (Tsh)</label><input type="number" name="group_existing_debt"></div>
                </div>
                <div class="form-row">
                    <div class="form-field"><label>Kikundi kimewahi kukopa?</label>
                        <div class="radio-group">
                            <label><input type="radio" name="previous_loan" value="NDIYO"> NDIYO</label>
                            <label><input type="radio" name="previous_loan" value="HAPANA"> HAPANA</label>
                        </div>
                    </div>
                    <div class="form-field"><label>Chanzo cha mapato</label><input type="text" name="income_source"></div>
                </div>
            </div>
        </div>
        
        <!-- PAGE 4: MDHAMINI NO.1 & NO.2 -->
        <div id="page4" class="page">
            <div class="section">
                <div class="section-title">5. TAARIFA ZA MDHAMINI NO. 1 (MWENYEKITI WA KIKUNDI)</div>
                <div class="form-row">
                    <div class="form-field"><label>Jina kamili la Mwenyekiti</label><input type="text" name="guarantor1_full_name"></div>
                    <div class="form-field"><label>Mahali Anapoishi</label><input type="text" name="guarantor1_residence"></div>
                </div>
                <div class="form-row">
                    <div class="form-field"><label>Namba ya nyumba</label><input type="text" name="guarantor1_house_number"></div>
                    <div class="form-field"><label>Amepanga/kwake</label>
                        <div class="radio-group">
                            <label><input type="radio" name="guarantor1_rent_status" value="Amepanga"> Amepanga</label>
                            <label><input type="radio" name="guarantor1_rent_status" value="Kwake"> Kwake</label>
                        </div>
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-field"><label>Kazi Anayofanya</label><input type="text" name="guarantor1_occupation"></div>
                    <div class="form-field"><label>Mahali ilipo Ofisi</label><input type="text" name="guarantor1_office_location"></div>
                </div>
                <div class="form-row">
                    <div class="form-field"><label>Jina la kampuni/biashara</label><input type="text" name="guarantor1_company"></div>
                    <div class="form-field"><label>Simu</label><input type="tel" name="guarantor1_phone"></div>
                </div>
            </div>
            
            <div class="section">
                <div class="section-title">MDHAMINI NO. 2 (MME, MKE AU NDUGU)</div>
                <div class="form-row">
                    <div class="form-field"><label>Jina kamili la Mdhamini</label><input type="text" name="guarantor2_full_name"></div>
                    <div class="form-field"><label>Mahali Anapoishi</label><input type="text" name="guarantor2_residence"></div>
                </div>
                <div class="form-row">
                    <div class="form-field"><label>Namba ya nyumba</label><input type="text" name="guarantor2_house_number"></div>
                    <div class="form-field"><label>Amepanga/kwake</label>
                        <div class="radio-group">
                            <label><input type="radio" name="guarantor2_rent_status" value="Amepanga"> Amepanga</label>
                            <label><input type="radio" name="guarantor2_rent_status" value="Kwake"> Kwake</label>
                        </div>
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-field"><label>Kazi Anayofanya</label><input type="text" name="guarantor2_occupation"></div>
                    <div class="form-field"><label>Mahali ilipo Ofisi</label><input type="text" name="guarantor2_office_location"></div>
                </div>
                <div class="form-row">
                    <div class="form-field"><label>Jina la kampuni/biashara</label><input type="text" name="guarantor2_company"></div>
                    <div class="form-field"><label>Simu</label><input type="tel" name="guarantor2_phone"></div>
                </div>
                <div class="form-row">
                    <div class="form-field"><label>Uhusiano (Mume, Mke, Ndugu, etc)</label><input type="text" name="guarantor2_relationship"></div>
                </div>
            </div>
        </div>
        
        <!-- PAGE 5: TAARIFA ZA DHAMANA (TABLE ONLY) -->
        <div id="page5" class="page">
            <div class="section">
                <div class="section-title">6. TAARIFA ZA DHAMANA</div>
                <table id="collateralTable">
                    <thead>
                        <tr>
                            <th>Aina ya Dhamana</th>
                            <th>Namba ya usajili</th>
                            <th>Thamani ya dhamana</th>
                            <th>Thamani yake kwa sasa</th>
                            <th>Umri</th>
                            <th>Mmiliki/wamiliki</th>
                            <th>Rangi/Muonekano</th>
                            <th>Mahali Ilipo</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody id="collateralBody">
                        <tr>
                            <td><input type="text" name="collateral_type[]" style="width:100%"></td>
                            <td><input type="text" name="collateral_reg_no[]" style="width:100%"></td>
                            <td><input type="number" name="collateral_value[]" style="width:100%"></td>
                            <td><input type="number" name="collateral_current_value[]" style="width:100%"></td>
                            <td><input type="number" name="collateral_age[]" style="width:100%"></td>
                            <td><input type="text" name="collateral_owner[]" style="width:100%"></td>
                            <td><input type="text" name="collateral_color[]" style="width:100%"></td>
                            <td><input type="text" name="collateral_location[]" style="width:100%"></td>
                            <td><button type="button" class="btn-remove" onclick="removeRow(this)">✗</button></td>
                        </tr>
                    </tbody>
                </table>
                <button type="button" class="btn-add" onclick="addCollateralRow()">+ Ongeza Dhamana Nyingine</button>
            </div>
        </div>
        
        <!-- PAGE 6: TAMKO NA SAHIHI -->
        <div id="page6" class="page">
            <div class="section">
                <div class="section-title">TAMKO LA MWOMBAJI</div>
                <div class="declaration">
                    <p>Mimi <input type="text" name="applicant_declaration_name" placeholder="Jina lako" style="width:200px"> nimeomba mkopo wa Tsh <input type="text" name="applicant_declaration_amount" placeholder="Kiasi" style="width:120px"> kutoka Orethan Microfinance. Nakiri kwamba taarifa zote nilizozitoa hapo juu ni sahihi kadiri ya ufahamu wangu. Pia nakubali kutembelewa na Afisa mikopo sehemu ya biashara yangu na nyumbani kwangu na kupata taarifa muhimu kutoka kwa watu wengine kwa ajili ya uhakiki wa taarifa zangu kwa matumizi ya ofisi.</p>
                    <p>Pia Kwa kujaza fomu hii natoa ridhaa kwa mkopeshaji kutoa taarifa zangu kwenye Taasisi za Kuchakata Taarifa za Wakopaji (CRB) na wadau wengine kama ilivyoanishwa kwenye sheria na miongozo inayotolewa na Benki Kuu Ya Tanzania pamoja na Tume ya Ulinzi wa Taarifa Binafsi.</p>
                </div>
                <div class="signature-area">
                    <div><div class="signature-line">SAHIHI</div><input type="text" name="applicant_signature" placeholder="Sahihi"></div>
                    <div><div class="signature-line">TAREHE</div><input type="date" name="applicant_date"></div>
                    <div><div class="signature-line">DOLE GUMBA</div><input type="text" name="applicant_thumbprint" placeholder="Alama ya gumba"></div>
                </div>
            </div>
            
            <div class="section">
                <div class="section-title">TAMKO LA MDHAMINI (MUME/MKE/NDUGU)</div>
                <div class="declaration">
                    <p>Mimi <input type="text" name="guarantor2_declaration_name" placeholder="Jina" style="width:150px"> Uhusiano <input type="text" name="guarantor2_declaration_relationship" placeholder="Uhusiano" style="width:100px"> ninakiri kuwa na taarifa juu ya mkopo wa Tsh <input type="text" name="guarantor2_declaration_amount" placeholder="Kiasi" style="width:100px"> uliyoombwa na <input type="text" name="guarantor2_declaration_applicant" placeholder="Jina la mwombaji" style="width:150px"> kutoka Orethan Microfinance. Dhamana tajwa hapo juu nazifahamu na nipo tayari zitolewe kama dhamana kwa mujibu wa masharti na taratibu zilizokubaliwa na mkopaji na mkopeshaji.</p>
                </div>
                <div class="signature-area">
                    <div><div class="signature-line">SAHIHI</div><input type="text" name="guarantor2_signature" placeholder="Sahihi"></div>
                    <div><div class="signature-line">DOLE GUMBA</div><input type="text" name="guarantor2_thumbprint" placeholder="Alama ya gumba"></div>
                    <div><div class="signature-line">TAREHE</div><input type="date" name="guarantor2_date"></div>
                </div>
            </div>
            
            <div class="section">
                <div class="section-title">TAMKO LA MDHAMINI (MWENYEKITI)</div>
                <div class="declaration">
                    <p>1. Mimi <input type="text" name="guarantor1_declaration_name" placeholder="Jina" style="width:150px"> nakubali kumdhamini <input type="text" name="guarantor1_declaration_applicant" placeholder="Jina la mwombaji" style="width:150px"> aliyeomba mkopo wa Tsh <input type="text" name="guarantor1_declaration_amount" placeholder="Kiasi" style="width:100px"> kutoka Orethan Microfinance. Nakiri kwamba taarifa zote nilizozitoa hapo juu ni sahihi kadiri ya ufahamu wangu. Pia, ninatambua na kukubali kwamba nitawajibika kulipa mkopo Pamoja na wajumbe wote wa kikundi endapo mkopaji atashindwa kulipa kama ilivyoainishwa kwenye mkataba.</p>
                </div>
                <div class="signature-area">
                    <div><div class="signature-line">SAHIHI</div><input type="text" name="guarantor1_signature" placeholder="Sahihi"></div>
                    <div><div class="signature-line">DOLE GUMBA</div><input type="text" name="guarantor1_thumbprint" placeholder="Alama ya gumba"></div>
                    <div><div class="signature-line">TAREHE</div><input type="date" name="guarantor1_date"></div>
                </div>
            </div>
            
            <div class="declaration" style="text-align:center;margin-top:20px">
                <p><strong>NB:</strong> KWA CHANGAMOTO AMA MALALAMIKO USISITE KUTUPIGIA KUPITIA</p>
                <p>Tel No.: (+255) 677 042 374 or (+255) 658 207 026</p>
            </div>
        </div>
        
        <!-- Navigation Buttons -->
        <div class="nav-buttons">
            <button type="button" class="btn-nav" id="prevBtn" onclick="changePage(-1)" style="display:none">← PREV</button>
            <button type="button" class="btn-nav" id="nextBtn" onclick="changePage(1)">NEXT →</button>
            <button type="submit" class="btn-nav btn-submit" id="submitBtn" style="display:none">✓ WASILISHA MAOMBI</button>
        </div>
    </form>
</div>

<script>
    let currentPage = 1;
    const totalPages = 6;
    
    function showPage(page) {
        for(let i = 1; i <= totalPages; i++) {
            let el = document.getElementById('page'+i);
            if(el) el.classList.remove('active');
        }
        let newPage = document.getElementById('page'+page);
        if(newPage) newPage.classList.add('active');
        
        for(let i = 1; i <= totalPages; i++) {
            let btn = document.querySelector('.page-btn:nth-child('+i+')');
            if(btn) {
                if(i === page) btn.classList.add('active');
                else btn.classList.remove('active');
            }
        }
        
        let prevBtn = document.getElementById('prevBtn');
        let nextBtn = document.getElementById('nextBtn');
        let submitBtn = document.getElementById('submitBtn');
        
        if(prevBtn) {
            if(page === 1) prevBtn.style.display = 'none';
            else prevBtn.style.display = 'inline-block';
        }
        
        if(nextBtn && submitBtn) {
            if(page === totalPages) {
                nextBtn.style.display = 'none';
                submitBtn.style.display = 'inline-block';
            } else {
                nextBtn.style.display = 'inline-block';
                submitBtn.style.display = 'none';
            }
        }
        currentPage = page;
    }
    
    function changePage(direction) {
        let newPage = currentPage + direction;
        if(newPage >= 1 && newPage <= totalPages) {
            showPage(newPage);
        }
    }
    
    function addCollateralRow() {
        let tbody = document.getElementById('collateralBody');
        if(!tbody) return;
        let newRow = tbody.insertRow();
        let fields = ['collateral_type', 'collateral_reg_no', 'collateral_value', 'collateral_current_value', 'collateral_age', 'collateral_owner', 'collateral_color', 'collateral_location'];
        
        for(let i = 0; i < fields.length; i++) {
            let cell = newRow.insertCell(i);
            let input = document.createElement('input');
            input.type = (i >= 2 && i <= 4) ? 'number' : 'text';
            input.name = fields[i] + '[]';
            input.style.width = '100%';
            cell.appendChild(input);
        }
        
        let actionCell = newRow.insertCell(fields.length);
        let removeBtn = document.createElement('button');
        removeBtn.type = 'button';
        removeBtn.className = 'btn-remove';
        removeBtn.innerHTML = '✗';
        removeBtn.onclick = function() { removeRow(this); };
        actionCell.appendChild(removeBtn);
    }
    
    function removeRow(btn) {
        let row = btn.closest('tr');
        if(row && row.parentNode && row.parentNode.children.length > 1) {
            row.remove();
        }
    }
</script>
</body>
</html>'''

with open('templates/group_loan_form.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('✅ NEW group loan form has REPLACED old one!')
print('📋 6 Pages with navigation | Table ONLY on Page 5')
