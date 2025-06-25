<<<<<<< HEAD
# bookstore-app



## Getting started

To make it easy for you to get started with GitLab, here's a list of recommended next steps.

Already a pro? Just edit this README.md and make it your own. Want to make it easy? [Use the template at the bottom](#editing-this-readme)!

## Add your files

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/topics/git/add_files/#add-files-to-a-git-repository) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://gitlab.com/phonepasit9/bookstore-app.git
git branch -M main
git push -uf origin main
```

## Integrate with your tools

- [ ] [Set up project integrations](https://gitlab.com/phonepasit9/bookstore-app/-/settings/integrations)

## Collaborate with your team

- [ ] [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
- [ ] [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
- [ ] [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
- [ ] [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- [ ] [Set auto-merge](https://docs.gitlab.com/user/project/merge_requests/auto_merge/)

## Test and Deploy

Use the built-in continuous integration in GitLab.

- [ ] [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/)
- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing (SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
- [ ] [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
- [ ] [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)

***

# Editing this README

When you're ready to make this README your own, just edit this file and use the handy template below (or feel free to structure it however you want - this is just a starting point!). Thanks to [makeareadme.com](https://www.makeareadme.com/) for this template.

## Suggestions for a good README

Every project is different, so consider which of these sections apply to yours. The sections used in the template are suggestions for most open source projects. Also keep in mind that while a README can be too long and detailed, too long is better than too short. If you think your README is too long, consider utilizing another form of documentation rather than cutting out information.

## Name
Choose a self-explaining name for your project.

## Description
Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.

## Badges
On some READMEs, you may see small images that convey metadata, such as whether or not all the tests are passing for the project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.

## Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Installation
Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
=======
# BookHaven App Structure

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
>>>>>>> ab26910 (Initial commit of existing project)
