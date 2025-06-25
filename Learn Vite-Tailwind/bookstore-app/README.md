# BookHaven App Structure

แอปพลิเคชัน BookHaven ถูกแบ่งออกเป็นส่วนต่างๆ เพื่อให้ง่ายต่อการดูแลและพัฒนาต่อ

## 📁 โครงสร้างโฟลเดอร์

```
src/
├── components/          # Components ที่ใช้ซ้ำได้
│   ├── Header.tsx      # ส่วนหัวเว็บไซต์
│   ├── BookCard.tsx    # การ์ดหนังสือแบบปกติ
│   ├── FeaturedBookCard.tsx  # การ์ดหนังสือแบบพิเศษ
│   ├── Footer.tsx      # ส่วนท้ายเว็บไซต์
│   └── index.ts        # Export ทั้งหมด
├── sections/           # ส่วนต่างๆ ของหน้าเว็บ
│   ├── SearchSection.tsx      # ส่วนค้นหา
│   ├── HeroSection.tsx        # ส่วนหลัก (Hero)
│   ├── FeaturedBooksSection.tsx  # ส่วนหนังสือแนะนำ
│   ├── NewReleasesSection.tsx    # ส่วนหนังสือใหม่
│   ├── CategoriesSection.tsx     # ส่วนหมวดหมู่
│   ├── WhyChooseSection.tsx      # ส่วนเหตุผลเลือกเรา
│   ├── CTASection.tsx           # ส่วน Call to Action
│   └── index.ts                 # Export ทั้งหมด
├── data/               # ข้อมูล Mock
│   ├── featuredBooks.ts
│   ├── newReleases.ts
│   ├── bookCategories.ts
│   ├── heroSlides.ts
│   ├── dropdownMenus.ts
│   └── index.ts
├── pages/              # หน้าต่างๆ
│   └── Home.tsx        # หน้าหลัก
└── README.md           # ไฟล์นี้
```

## 🧩 Components

### Header.tsx
- ส่วนหัวเว็บไซต์พร้อมเมนูนำทาง
- รองรับการแสดงผลบนมือถือ
- มี dropdown menus สำหรับการนำทาง

### BookCard.tsx
- การ์ดแสดงหนังสือแบบปกติ
- แสดงรูปภาพ, ชื่อ, ผู้แต่ง, ราคา
- มีปุ่ม Add to Cart และ Wishlist

### FeaturedBookCard.tsx
- การ์ดหนังสือแบบพิเศษ (แนวนอน)
- แสดงรายละเอียดเพิ่มเติม
- เหมาะสำหรับหนังสือแนะนำ

### Footer.tsx
- ส่วนท้ายเว็บไซต์
- ลิงก์ต่างๆ และข้อมูลติดต่อ

## 📄 Sections

### SearchSection.tsx
- ส่วนค้นหาหนังสือ
- มีปุ่มค้นหาด่วนตามหมวดหมู่

### HeroSection.tsx
- ส่วนหลักของหน้าเว็บ
- Carousel แสดงข้อความหลัก
- มีปุ่ม Call to Action

### FeaturedBooksSection.tsx
- แสดงหนังสือแนะนำ
- ใช้ FeaturedBookCard component

### NewReleasesSection.tsx
- แสดงหนังสือใหม่
- ใช้ BookCard component

### CategoriesSection.tsx
- แสดงหมวดหมู่หนังสือ
- มีไอคอนและสีสันสวยงาม

### WhyChooseSection.tsx
- แสดงเหตุผลเลือก BookHaven
- มีไอคอนและคำอธิบาย

### CTASection.tsx
- ส่วน Call to Action
- ชวนให้สมัครสมาชิก

## 🎯 ประโยชน์ของการแยกส่วน

1. **ง่ายต่อการดูแล**: แต่ละส่วนมีหน้าที่ชัดเจน
2. **นำกลับมาใช้ได้**: Components สามารถใช้ซ้ำได้
3. **แก้ไขง่าย**: แก้ไขส่วนใดส่วนหนึ่งโดยไม่กระทบส่วนอื่น
4. **ทำงานเป็นทีม**: แต่ละคนสามารถทำงานคนละส่วนได้
5. **ทดสอบง่าย**: ทดสอบแต่ละส่วนแยกกันได้

## 📝 วิธีการใช้งาน

```typescript
// Import components
import { Header, BookCard, Footer } from '../components';

// Import sections
import { SearchSection, HeroSection } from '../sections';

// Import data
import { featuredBooks, newReleases } from '../data';
```

## 🔧 การเพิ่มส่วนใหม่

1. สร้างไฟล์ใหม่ใน `components/` หรือ `sections/`
2. Export จาก `index.ts`
3. Import และใช้งานใน `Home.tsx`

โครงสร้างนี้ทำให้โค้ดเป็นระเบียบและง่ายต่อการพัฒนาต่อ! 🚀 