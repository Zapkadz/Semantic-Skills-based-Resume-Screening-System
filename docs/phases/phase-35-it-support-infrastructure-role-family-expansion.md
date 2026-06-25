# Phase 35 - IT Support / Infrastructure Role-family Expansion

## 1. Muc tieu phase

Sau Phase 34, he thong da co kha nang:

- phat hien technical signals trong responsibilities;
- promote mot phan responsibilities technical-rich vao scoring input;
- dua promoted unknown requirements vao open-set path.

Noi ngan gon:

```text
Phase 33 = thay technical signals trong responsibilities
Phase 34 = dua mot phan signal do vao matching/scoring input
Phase 35 = hieu ro hon "day la nghe gi" de promotion va matching bot mu mo
```

Muc tieu cua Phase 35 la:

```text
Mo rong role-family coverage cho nhom IT Support / Helpdesk / Infrastructure,
de he thong khong con roi ve GENERIC_TECH qua som
khi gap cac JD van hanh ha tang, support he thong, sysadmin hoac network support.
```

Rat quan trong:

```text
Phase 35 sua role-family inference va role-aware intent coverage,
nhung chua sua score formula / source-aware weighting.
```

Tuc la:

- cho phep he thong nhan role dung hon;
- cho phep technical signals trong responsibilities duoc dat trong dung ngu canh nghe;
- nhung calibration diem chi tiet van de cho Phase 36.

## 2. Vi tri cua Phase 35 trong cay dependency

Day la phase thu ba trong nhanh sua section-aware JD sourcing va role-awareness:

```text
Phase 33 -> Responsibility signal extraction foundation
Phase 34 -> Controlled responsibility-to-requirement promotion
Phase 35 -> IT support / infra role-family expansion
Phase 36 -> Source-aware scoring calibration
Phase 37 -> Confidence and diagnostics guardrails
Phase 38 -> Benchmark and regression pack
```

Nguyen tac de khong bi lech huong:

```text
Phase 35 chi sua:
- role-family schema
- role-family inference signals
- role-aware technical intent coverage

Phase 35 chua sua:
- score formula
- hard-skill gate weight
- review card wording lon
- admin taxonomy workflow lon
```

## 3. Van de can giai quyet

### 3.1 Nhieu JD support / infra dang roi ve `GENERIC_TECH`

Job 22 va cac case tuong tu cho thay:

- title co chua `IT Support`, `IT Helpdesk`, `IT Staff`
- responsibilities co:
  - Active Directory
  - DNS
  - DHCP
  - Firewall
  - Router
  - Switch
  - VPN
  - Google Workspace
  - Virtualization

Nhung role-family hien tai chua co "nha" tot cho cum nay,
nen he thong de:

```text
primary_role_family = GENERIC_TECH
```

Dieu nay lam:

- promotion gate mat mot lop ngu canh quan trong;
- requirement intent con mo;
- explanation chua giai thich dung nghe nghiep thuc te.

### 3.2 Hien tai `DEVOPS_CLOUD` va `SECURITY_GRC` chua thay the duoc role infra support

Nhieu term ha tang nhin qua co ve gan voi:

- `DEVOPS_CLOUD`
- `SECURITY_GRC`

Nhung ve nghiep vu,
role:

- IT Support
- Helpdesk
- Infrastructure Support
- Sysadmin / System Operations
- Network Support

khac voi:

- DevOps engineer
- Cloud engineer
- Governance / compliance security

Neu khong tach ro,
he thong de:

- doan nham role;
- overfit mot so skill sang sai nhom nghe;
- khien recruiter thay explanation "khong dung chat cong viec".

### 3.3 Promotion gate o Phase 34 da co, nhung van chua "biet nghe"

Phase 34 da promotion duoc requirement technical sparse.
Nhung hien tai gate van con kha bao thu va generic:

- thay technical signal manh thi promote;
- nhung chua hieu signal nao la core cho helpdesk/infra,
  signal nao chi la ngoai bien.

Vi du:

```text
VPN
Firewall
AD
DNS
DHCP
```

voi backend role la peripheral,
nhung voi helpdesk/infra role lai co the la core.

### 3.4 Technical intent hien tai chua phan loai sau cho nhom support / infra

Phase 29-30 da co `requirement_intent_summary`,
nhung intent mapping hien tai manh hon cho:

- Backend
- Computer Vision / eKYC
- Security GRC
- DevOps Cloud

Con nhom support / infrastructure thi chua du:

- system administration
- endpoint support
- network operations
- workplace tooling
- identity/access administration o muc support

## 4. Vi sao Phase 35 la buoc tiep theo dung nhat

Sau Phase 34, he thong da co the dua:

- `Active Directory`
- `DNS`
- `DHCP`
- `Firewall`

vao open-set requirement path.

Nhung neu van chua co role-family phu hop,
thi he thong moi chi biet:

```text
day la technical requirements
```

ma chua biet:

```text
day la technical requirements thuoc nhom nghe support / infrastructure
```

Neu nhay thang sang Phase 36 scoring calibration luc nay,
thi scorer se phai calibration tren mot role-family van con generic.

Noi cach khac:

```text
Phase 34 tao duoc technical core
Phase 35 moi dat technical core do vao dung nghe nghiep
```

Vi vay Phase 35 la buoc tiep theo hop ly nhat.

## 5. Nguyen tac thiet ke

### 5.1 Mo rong role-family, nhung khong bung qua nhieu nhanh moi

Khong nen tao qua nhieu role-family manh mun ngay.

Phase 35 nen giu tap mo rong nho, on dinh, de benchmark duoc.

Huong de xuat:

- `IT_SUPPORT_INFRA`

va co the de sau nay tach nho hon neu that su can:

- `HELPDESK_SUPPORT`
- `SYSADMIN_INFRA`
- `NETWORK_SUPPORT`

Nhung o Phase 35,
uu tien 1 role-family gop la hop ly hon.

### 5.2 Role-family moi phai giai thich duoc bang term that

Role-family `IT_SUPPORT_INFRA` nen co:

- title terms ro;
- core terms ro;
- supporting terms ro;
- relation hop ly voi role khac.

Neu khong giai thich duoc bo term,
thi role-family moi se chi la "ten goi dep" ma khong co gia tri nghiep vu.

### 5.3 Uu tien workplace/system/network operations

Phase 35 nen cover cac nhom tin hieu sau:

- identity/workplace administration
  - Active Directory
  - account provisioning
  - Google Workspace
  - Microsoft 365
- network support
  - DNS
  - DHCP
  - router
  - switch
  - VPN
  - WiFi controller
- server/system operations
  - server
  - Windows Server
  - Linux administration
  - virtualization
  - VMware
  - Hyper-V
- support operations
  - troubleshooting
  - incident handling
  - end-user support

### 5.4 Khong bien support/infra thanh DevOps cloud

Can co guard de tranh viec:

- co `Linux`
- co `server`
- co `network`

la bi suy ra `DEVOPS_CLOUD`.

Vi thuc te:

- DevOps nghieng ve automation, CI/CD, infra-as-code, cloud runtime
- IT support / infra nghieng ve admin, support, troubleshooting, workplace/system/network operations

### 5.5 Backward-compatible voi role families cu

Phase 35 khong duoc lam vo:

- backend cases
- AI / CV cases
- security GRC cases
- devops cases

Muc tieu la:

```text
them mot role-family dung cho infra/support
ma khong lam sai nhung role-family da on
```

## 6. Kien truc de xuat

### 6.1 Cap nhat role-family schema

Them role-family moi:

```text
IT_SUPPORT_INFRA
```

vao:

- `ROLE_FAMILIES`
- `ROLE_FAMILY_DEFINITIONS`
- `RELATED_ROLE_FAMILIES`

### 6.2 Title terms de xuat

Vi du:

- `it support`
- `helpdesk`
- `help desk`
- `it helpdesk`
- `it support engineer`
- `it support specialist`
- `system administrator`
- `sysadmin`
- `infrastructure engineer`
- `it infrastructure`
- `network support`
- `desktop support`

### 6.3 Core terms de xuat

Vi du:

- `active directory`
- `dns`
- `dhcp`
- `firewall`
- `router`
- `switch`
- `vpn`
- `google workspace`
- `microsoft 365`
- `office 365`
- `virtualization`
- `vmware`
- `hyper-v`
- `windows server`
- `linux administration`
- `server administration`
- `troubleshooting`
- `incident support`
- `end user support`

### 6.4 Supporting terms de xuat

Vi du:

- `sap`
- `printer`
- `hardware`
- `software installation`
- `ticketing`
- `monitoring`
- `user account`
- `access provisioning`

### 6.5 Related role-family de xuat

`IT_SUPPORT_INFRA` nen co quan he gan voi:

- `DEVOPS_CLOUD` (co giao nhau o ha tang, nhung khac kieu cong viec)
- `SECURITY_GRC` (co giao nhau o access / compliance support)
- `GENERIC_TECH`

nhung khong nen bi coi la dong nhat.

## 7. Cap nhat technical intent cho role-family moi

Ngoai role-family inference,
Phase 35 nen mo rong `technical_intent` cho nhom nay.

Vi du:

- `Active Directory` -> `INFRA_IDENTITY_ADMIN`
- `DNS`, `DHCP`, `VPN`, `Firewall` -> `NETWORK_OPERATIONS`
- `Virtualization`, `VMware`, `Windows Server` -> `SYSTEM_OPERATIONS`
- `Google Workspace`, `Microsoft 365` -> `WORKPLACE_ADMIN`

Khong can qua chi tiet ngay,
nhung can du de:

- requirement_intent_summary biet "term nay dung chat support/infra"
- role-family alignment sac hon
- explanation hop ly hon

## 8. File du kien sua

### Sua chinh

```text
src/role_family.py
src/technical_intent.py
```

### Co the sua nhe

```text
src/jd_parser.py
src/requirement_extractor.py
src/responsibility_signal_extractor.py
```

neu can them mot vai term ho tro role inference tot hon.

### Test

```text
tests/test_role_family.py
tests/test_technical_intent.py
tests/test_payload_pipeline.py
tests/test_core_logic_benchmark.py
```

Neu can,
co the them fixture benchmark nho cho:

- helpdesk/support sparse JD
- infrastructure support JD
- network support JD

## 9. Expected behavior sau phase

Sau Phase 35,
cac JD kieu:

- IT Staff
- IT Support
- Helpdesk
- Infrastructure Support
- System Administrator

nen co xu huong:

```text
primary_role_family = IT_SUPPORT_INFRA
```

thay vi:

```text
GENERIC_TECH
```

Dong thoi:

- `requirement_intent_summary` nen co them cac intent phu hop voi support/infra;
- promoted requirements o Phase 34 duoc dat vao ngu canh nghe dung hon;
- explanation sau nay co nen tang tot hon cho Phase 36-37.

## 10. Benchmark can khoa o Phase 35

Can co benchmark cho it nhat 5 nhom:

### 10.1 Helpdesk / IT Support sparse JD

Case giong Job 22.

Ky vong:

- role-family = `IT_SUPPORT_INFRA`
- promoted technical requirements duoc giai nghia dung hon

### 10.2 System administration / infrastructure JD

Vi du:

- Windows Server
- VMware
- virtualization
- AD / DNS / DHCP

Ky vong:

- role-family nghieng ve `IT_SUPPORT_INFRA`

### 10.3 Network support / operations JD

Vi du:

- router
- switch
- firewall
- VPN
- WiFi

Ky vong:

- role-family van map ve `IT_SUPPORT_INFRA`
- khong troi sang `SECURITY_GRC` chi vi co firewall/VPN

### 10.4 DevOps / Cloud jobs dang on

Ky vong:

- van o `DEVOPS_CLOUD`
- khong bi hut sang `IT_SUPPORT_INFRA`

### 10.5 Security / Governance jobs dang on

Ky vong:

- van o `SECURITY_GRC`
- khong bi hut sang `IT_SUPPORT_INFRA`

## 11. Risk va cach chan regression

### 11.1 Overlap voi DevOps

Nguy co:

- `Linux`, `server`, `infrastructure`

la term giao nhau.

Cach chan:

- DevOps can term manh hon nhu:
  - CI/CD
  - Kubernetes
  - Terraform
  - AWS/Azure/GCP
  - Prometheus/Grafana
- Support/infra can term manh hon nhu:
  - Active Directory
  - DNS/DHCP
  - router/switch
  - end-user support
  - virtualization

### 11.2 Overlap voi Security

Nguy co:

- `firewall`
- `access`
- `security`

co the lam role support bi hut sang `SECURITY_GRC`.

Cach chan:

- GRC can term manh hon nhu:
  - governance
  - compliance
  - risk management
  - audit
  - Qualys
  - ISO 27001
- Support/infra can term van hanh / admin / troubleshooting ro hon.

### 11.3 Over-specialization qua som

Nguy co:

- role-family moi qua nho
- benchmark it
- heuristic vo som

Cach chan:

- Phase 35 chi them 1 family gop `IT_SUPPORT_INFRA`
- chua tach thanh 3-4 sub-family ngay.

## 12. Dependency sanity check trong qua trinh code

Moi khi code Phase 35, can hoi nguoc 5 cau:

1. Minh dang sua role-family hay da len tay sang scoring calibration?
2. Case helpdesk/infra co that su thoat khoi `GENERIC_TECH` khong?
3. DevOps va Security jobs co bi hut sai sang role-family moi khong?
4. Technical intent cho AD/DNS/DHCP/VPN co sac hon khong?
5. Promotion gate o Phase 34 co duoc huong dan boi role-family dung hon khong?

Neu trong qua trinh code phat hien:

- can them 1 role term nho;
- can them 1 intent bucket nho;
- can them 1 fixture benchmark nho;

thi co the bo sung ngay trong Phase 35,
mien la van giu boundary:

```text
role-family coverage va technical intent coverage
chu chua dong vao score formula
```

## 13. Pham vi thuc hien cua Phase 35

Phase 35 nen tap trung:

- them role-family `IT_SUPPORT_INFRA`
- mo rong role-family inference rules
- mo rong technical intent mapping cho support/infra terms
- benchmark helpdesk/infra va regression tren backend/devops/security

Phase 35 chua nen:

- sua weight scoring;
- them source-aware score weighting;
- sua diagnostics UI lon;
- sua admin workflow lon.

## 14. Phase 35 duoc xem la hoan thanh khi

1. Helpdesk / infra sparse JD khong con roi ve `GENERIC_TECH` trong da so case benchmark.
2. DevOps / Security / Backend jobs van giu role-family hop ly.
3. `requirement_intent_summary` co sach hon voi support/infra terms.
4. Benchmark Phase 26-34 van pass.
5. Co test moi khoa lai role-family expansion cho nhom support/infra.

## 15. Gia tri bao cao do an

Phase 35 co gia tri lon khi bao cao vi co the giai thich:

```text
He thong khong chi match ky nang ky thuat,
ma con dat ky nang do vao dung nhom nghe nghiep.
```

Voi nhom IT Support / Infrastructure, day la dieu rat quan trong,
vi cung la term ky thuat nhung:

- `VPN`, `DNS`, `DHCP`, `AD`

co vai tro core voi support/infra,
nhung khong the duoc giai thich giong DevOps hay Security governance.

## 16. Huong sau Phase 35

Neu Phase 35 xong dung huong,
phase tiep theo hop ly nhat la:

```text
Phase 36 - Source-aware Scoring Calibration
```

Phase 36 se tap trung:

- explicit requirement vs promoted responsibility vs semantic-only
- dieu chinh score theo nguon requirement
- tranh score ao sau khi Phase 34-35 da mo rong technical core va role context.
