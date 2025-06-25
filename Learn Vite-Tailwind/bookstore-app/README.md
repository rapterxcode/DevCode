# BookHaven App Structure

## Deverlop by Phone RapterXCode :D
แอปพลิเคชัน BookHaven ถูกแบ่งออกเป็นส่วนต่างๆ เพื่อให้ง่ายต่อการดูแลและพัฒนาต่อ

## 🚀 การติดตั้งและรันโปรเจค

### Prerequisites
- Node.js (เวอร์ชัน 18 หรือใหม่กว่า)
- npm หรือ yarn

### การติดตั้ง (Installation)

1. **Clone โปรเจค**
```bash
git clone <repository-url>
cd bookstore-app
```

2. **ติดตั้ง Dependencies**
```bash
npm install
# หรือ
yarn install
```

### การรันโปรเจค (Development)

```bash
npm run dev
# หรือ
yarn dev
```

แอปจะรันที่ `http://localhost:5173` (หรือพอร์ตอื่นที่ Vite กำหนด)

### การ Build โปรเจค (Production)

```bash
npm run build
# หรือ
yarn build
```

ไฟล์ที่ build แล้วจะอยู่ในโฟลเดอร์ `dist/`

### การ Preview Production Build

```bash
npm run preview
# หรือ
yarn preview
```

### การ Lint โค้ด

```bash
npm run lint
# หรือ
yarn lint
```

## 📦 Dependencies หลัก

### Core Dependencies
- **React** `^19.1.0` - UI Library
- **React DOM** `^19.1.0` - React DOM rendering
- **React Router DOM** `^7.6.2` - Client-side routing

### Build Tools & Development
- **Vite** `^6.3.5` - Build tool และ Development server
- **TypeScript** `~5.8.3` - Type safety
- **@vitejs/plugin-react** `^4.4.1` - React plugin for Vite

### Styling & UI
- **Tailwind CSS** `^3.4.17` - Utility-first CSS framework
- **Material Tailwind** `^2.1.10` - UI Components library
- **@material-tailwind/html** `^3.0.0-beta.7` - Material Tailwind HTML components
- **PostCSS** `^8.5.6` - CSS processing
- **Autoprefixer** `^10.4.21` - CSS vendor prefixing

### Icons & Assets
- **Iconoir React** `^7.11.0` - Icon library

### Development Dependencies
- **ESLint** `^9.25.0` - Code linting
- **@types/react** `^19.1.2` - React TypeScript definitions
- **@types/react-dom** `^19.1.2` - React DOM TypeScript definitions
- **vite-plugin-checker** `^0.9.3` - Type checking plugin

### Node.js Version
- **Node.js** - เวอร์ชัน 18 หรือใหม่กว่า (แนะนำ Node.js 18+)

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