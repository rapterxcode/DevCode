# Data Structure Documentation

This folder contains all the mock data for the BookHaven bookstore application, organized into separate files for better maintainability and reusability.

## File Structure

### `index.ts`
Main export file that re-exports all data and types from individual files for easy importing.

### `dropdownMenus.ts`
Contains the dropdown menu structure and navigation data.
- **Exports**: `DropdownItem`, `DropdownMenu`, `DropdownMenus` interfaces
- **Function**: `createDropdownMenus()` - Creates dropdown menus with scroll functions

### `featuredBooks.ts`
Contains the featured books data with detailed information.
- **Exports**: `Book` interface, `featuredBooks` array
- **Data**: Book details including title, author, price, images, ratings, etc.

### `newReleases.ts`
Contains new release books data.
- **Exports**: `newReleases` array
- **Data**: New books with `isNew` flag and additional metadata

### `bookCategories.ts`
Contains book category/genre information.
- **Exports**: `BookCategory` interface, `bookCategories` array
- **Data**: Genre categories with icons, colors, and book counts

### `heroSlides.ts`
Contains hero section carousel data.
- **Exports**: `HeroSlide` interface, `heroSlides` array
- **Data**: Carousel slides with titles, descriptions, and styling

### `searchData.ts`
Contains search section configuration and quick search categories.
- **Exports**: `SearchCategory`, `SearchData` interfaces, `searchData` object
- **Data**: Search title, subtitle, placeholder text, button text, and quick search categories

### `whyChooseData.ts`
Contains "Why Choose Us" section configuration and features.
- **Exports**: `WhyChooseFeature`, `WhyChooseData` interfaces, `whyChooseData` object
- **Data**: Section title, subtitle, and list of features with icons and descriptions

### `footerData.ts`
Contains footer configuration including brand info, navigation links, and social media links.
- **Exports**: `FooterLink`, `FooterSection`, `SocialLink`, `FooterData` interfaces, `footerData` object
- **Data**: Brand information, navigation sections, social media links, and copyright text

### `headerData.ts`
Contains header navigation, action buttons, and auth buttons.
- **Exports**: `HeaderButton`, `HeaderData` interfaces
- **Data**: Brand information, navigation buttons, action buttons, and auth buttons

## Usage

```typescript
// Import all data
import { 
  featuredBooks, 
  newReleases, 
  bookCategories, 
  heroSlides,
  searchData,
  whyChooseData,
  footerData,
  createDropdownMenus,
  headerData
} from '../data';

// Import specific types
import type { Book, BookCategory, HeroSlide, SearchData, WhyChooseData, FooterData, HeaderData } from '../data';
```

## Data Interfaces

### Book
```typescript
interface Book {
  id: number;
  title: string;
  author: string;
  genre: string;
  price: number;
  originalPrice?: number;
  image: string[];
  rating: number;
  description: string;
  color: string;
  isNew?: boolean;
}
```

### BookCategory
```typescript
interface BookCategory {
  id: number;
  name: string;
  icon: string;
  color: string;
  books: string;
  description: string;
}
```

### HeroSlide
```typescript
interface HeroSlide {
  id: number;
  title: string;
  subtitle: string;
  cta: string;
  bg: string;
  icon: string;
}
```

### SearchData
```typescript
interface SearchData {
  title: string;
  subtitle: string;
  placeholder: string;
  searchButtonText: string;
  quickSearchCategories: SearchCategory[];
}

interface SearchCategory {
  id: number;
  name: string;
  icon: string;
  description?: string;
}
```

### WhyChooseData
```typescript
interface WhyChooseData {
  title: string;
  subtitle: string;
  features: WhyChooseFeature[];
}

interface WhyChooseFeature {
  id: number;
  icon: string;
  title: string;
  description: string;
}
```

### FooterData
```typescript
interface FooterData {
  brand: {
    name: string;
    icon: string;
    description: string;
  };
  sections: FooterSection[];
  socialLinks: SocialLink[];
  socialDescription: string;
  copyright: string;
}

interface FooterSection {
  id: number;
  title: string;
  links: FooterLink[];
}

interface FooterLink {
  id: number;
  name: string;
  url: string;
}

interface SocialLink {
  id: number;
  name: string;
  icon: string;
  url: string;
}
```

### HeaderData
```typescript
interface HeaderButton {
  id: number;
  icon: string;
  label: string;
  action?: () => void;
  badge?: number;
  type: 'navigation' | 'action' | 'auth';
}

interface HeaderData {
  brand: {
    name: string;
    icon: string;
  };
  navigationButtons: HeaderButton[];
  actionButtons: HeaderButton[];
  authButtons: HeaderButton[];
}
```

## Benefits of This Structure

1. **Separation of Concerns**: Each data type is in its own file
2. **Type Safety**: Strong TypeScript interfaces for all data
3. **Reusability**: Data can be imported and used across components
4. **Maintainability**: Easy to update specific data without affecting others
5. **Scalability**: Easy to add new data types or modify existing ones
6. **Testing**: Individual data files can be easily mocked for testing 