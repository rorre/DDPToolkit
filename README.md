# DDP Toolkit

See also: [LIT's Moss for DDP](https://github.com/asfiowilma/Moss-For-DDP)

## Why This Sucks

- Penamaan file sering salah
- Check akan dianggap gagal jika ada lebih/kurang spasi atau baris baru
- Depends on DDPValidator, yang bloated
- I, Ren, harus menambahkan testcase ke [registry](https://github.com/rorre/DDPValidator/tree/main/data) (Kamu bisa buka PR, tho)

## Why This Is Cool

- Kamu malas  
  ... untuk membuka satu-satu dan reinput semua test case
- Ada perbandingan I/O side-by-side, [lihat di sini](https://github.com/rorre/DDPValidator#error-diff)
- Kamu ingin memfilter semua yang bukan kamu urus dalam asdos.
- Review code sebelum menjalankan test

## How

- Download latest release DDPValidator [di sini](https://github.com/rorre/DDPValidator/releases/latest)
- Taro executable di folder yang sama dengan `validator.py` (atau direktori PATH)
- Buat config.json seperti sample di bawah
- Download semua submission dengan meng-klik `Download All Submissions`  
  ![](https://d.rorre.xyz/XGkZJLNUG/chrome_pIm2UHfFt5.png)
- Extract ke folder `submissions`
- `python validator.py filter` -- Filter asdos, kelas, dan penamaan tidak valid ke folder `invalid`
- `python validator.py extract` -- Extract semua zip di `submission`, skip jika submisi berbentuk file `.py`
- `python validator.py run` -- Menjalankan semua submission

## `config.json`

```json
{
  "kelas": "H",
  "asdos": "REN",
  "editor": "code" // atau nvim, vim, nano, vi
}
```
