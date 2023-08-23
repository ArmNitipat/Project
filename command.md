<?php echo"# Project" >> READMY";?>
===========================================================================================================
Git Status
===========================================================================================================
Untracked สถานะไฟล์ยังไม่ได้ถูกจัดเก็บไว้ในระบบ git
Working Directory สถานะที่มีการเปลี่ยนเเปลงหนือเเก้ไชไฟล์
Staged สถานะเตรียม Commit เพื่อยืนยันการเเปลี่ยนเเปลงก่อนเก็บลงในสถานะ(Local Repositore)
Local Repository สถานะเก็บบันทึกข้อมูล ไฟล์ที่เปลี่ยนเเปลงลงใน git Repository เเบบ Local (ที่เครื่องตัวเอง)
Remote Repository สถานะเก็บบันทึกข้อมูล ไฟล์ที่เปลี่ยนเเปลงลงใน git Repository เเบบ  Hosting(ที่เครื่องเซิร์ฟเวอร์)
===========================================================================================================
Untracked  Working Directory  Staged  Local Repositore  Remote Repositore 
   (1)            (2)           (3)         (4)                (5)
===========================================================================================================
git init -> #สร้าง repository ใหม่ในโฟลเดอร์ปัจจุบัน
git add index.html  ->  #เฉพาะไฟล์เพิ่มเข้า สถาณะ Staged
git add .  ->  #ทุกไฟล์
git reset index.html ->  #เป็นคำสั่งที่ใช้สำหรับการย้อนกลับการเปลี่ยนแปลง
้git commit -m "message"  ->  #ยืนยันการเเปลี่ยนเเปลง
git Clean -n  ->  #เเสดง Source Code ที่อยู่ในสถานะ Untracked 
git Clean -df  ->  #ลบ  Source Code ที่อยู่ในสถานะ Untracked
git status -> #แสดงสถานะของไฟล์ใน workspace เมื่อเทียบกับ staging area
git log  ->  #แสดงประวัติการ commit
git remote  -v  #เเสดงการเชื่อมต่อกับใคร
git remote add origin https://_____  ->  #เชื่อมต่อกับภายนอก
git push origin ชื่อ  ->  #ส่งการเปลี่ยนแปลงใน local repository ไปยัง remote repository
git pull origin ชื่อ  ->  #ดึงการเปลี่ยนแปลงจาก remote repository
git branch ชื่อ  ->  #สร้าง branch ใหม่
git branch -d ชื่อ  ->  #ลบ branch อย่างปลอดภัย
git Checkout  ->  #สลับ branch หรือ commit ID
git merge --no--ff #ใช้เพื่อรวม branches โดยสร้าง commit merge ใหม่เสมอ ("no fast-forward")
git merge  ->  #ใช้รวม branches หรือ commits
===========================================================================================================
<a href = "https://drive.google.com/file/d/1ct77nIFNMuUC0dUKU5fTjFV8OiTXTFpE/view"></a>