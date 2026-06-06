# Refactoring Plan - Phase 01

## 1. Muc tieu refactor

Muc tieu chi la cai thien chat luong code va tai lieu neu can, khong thay doi hanh vi he thong.

O Phase 01, code moi chi co entry point toi thieu va cau truc thu muc nen tang, nen chua co nhu cau refactor lon.

## 2. Nguyen tac bat buoc

- Khong thay doi behavior hien tai.
- Giu API compatibility.
- Khong thay doi input/output da thong nhat.
- Khong doi cong thuc scoring vi Phase 01 chua co scoring.
- Khong doi flow nghiep vu.
- Chi refactor sau khi da co test hoac huong dan test ro rang.

## 3. Cac van de code can xem xet

### 3.1 Duplication

Hien tai co mot it chuoi thong tin du an lap lai giua `main.py` va `app.py`, nhu ten project va phase hien tai.

Vi Phase 01 chi la foundation va chua co module config, chua can tach thanh file cau hinh rieng.

### 3.2 Oversized files

Khong co file code qua lon.

- `main.py` chi la CLI placeholder.
- `app.py` chi la Streamlit placeholder.
- README va learning log co dung muc tieu tai lieu.

### 3.3 Naming

Ten file va bien hien tai ro rang:

- `PROJECT_NAME`
- `CURRENT_PHASE`
- `build_parser`
- `main`

Chua can doi naming.

### 3.4 Missing tests

Phase 01 chua co automated tests vi chua co business logic. Test thu cong la phu hop:

- `python main.py --help`
- `python main.py`
- `python app.py`

Automated tests nen bat dau tu Phase 02 khi co `document_loader.py`.

### 3.5 API compatibility

Chua co public API nghiep vu. Neu refactor luc nay, can giu nguyen:

- `main.py` van la CLI entry point.
- `app.py` van la Streamlit entry point.
- `src/` van la package source chinh.

## 4. De xuat refactor

### De xuat 1 - Chua refactor ngay

- File lien quan: `main.py`, `app.py`
- Van de: co lap lai nhe thong tin `PROJECT_NAME` va `CURRENT_PHASE`.
- Cach refactor: co the tach constants sang `src/config.py` trong phase sau.
- Rui ro: tao abstraction qua som khi chua co logic that su.
- Cach test sau refactor: chay lai `python main.py --help`, `python main.py`, `python app.py`.
- Co thay doi behavior khong? Khong.

Ket luan: khong nen refactor trong Phase 01. Nen giu code don gian de nguoi hoc de doc.

### De xuat 2 - Them automated test sau khi co module dau tien

- File lien quan: `tests/`, Phase 02 `src/document_loader.py`.
- Van de: Phase 01 chua co test tu dong.
- Cach refactor: khong refactor Phase 01; them test trong Phase 02 khi co function doc file text.
- Rui ro: them test qua som cho placeholder se it gia tri.
- Cach test sau refactor: chay `pytest`.
- Co thay doi behavior khong? Khong.

Ket luan: de sang Phase 02.

## 5. Pham vi refactor

Phase 01 khong thuc hien refactor code.

Khong refactor:

- Khong tach constants sang file config.
- Khong them test placeholder.
- Khong doi README, phase plan hay learning log neu khong co loi.
- Khong them logic document loader.

## 6. Ke hoach test sau refactor

Vi khong de xuat refactor ngay, chi can giu ket qua test Phase 01:

```bash
python main.py --help
python main.py
python app.py
git status --short --branch
```

Neu sau nay refactor constants hoac entry point, can chay lai cac lenh tren de dam bao behavior khong doi.

## 7. Ghi chu cho bao cao

Sau moi phase, du an co buoc xem xet refactor de dam bao code de bao tri va de mo rong. Trong Phase 01, code con rat nho nen viec khong refactor la lua chon phu hop. Dieu nay giup tranh tao abstraction qua som, dong thoi van giu quy trinh review chat luong code mot cach chuyen nghiep.
