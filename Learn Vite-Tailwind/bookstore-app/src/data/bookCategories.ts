export interface BookCategory {
  id: number;
  name: string;
  icon: string;
  color: string;
  books: string;
  description: string;
}

export const bookCategories: BookCategory[] = [
  { 
    id: 1, 
    name: "Fiction", 
    icon: "📚", 
    color: "from-blue-500 to-indigo-600", 
    books: "12,500+", 
    description: "Imaginative stories and novels" 
  },
  { 
    id: 2, 
    name: "Non-Fiction", 
    icon: "📖", 
    color: "from-green-500 to-emerald-600", 
    books: "8,200+", 
    description: "Real stories and knowledge" 
  },
  { 
    id: 3, 
    name: "Mystery & Thriller", 
    icon: "🔍", 
    color: "from-purple-500 to-pink-600", 
    books: "5,800+", 
    description: "Suspense and intrigue" 
  },
  { 
    id: 4, 
    name: "Romance", 
    icon: "💕", 
    color: "from-pink-500 to-rose-600", 
    books: "7,300+", 
    description: "Love stories and passion" 
  },
  { 
    id: 5, 
    name: "Science Fiction", 
    icon: "🚀", 
    color: "from-cyan-500 to-blue-600", 
    books: "4,600+", 
    description: "Future worlds and technology" 
  },
  { 
    id: 6, 
    name: "Biography", 
    icon: "👤", 
    color: "from-orange-500 to-red-600", 
    books: "3,900+", 
    description: "Real lives and stories" 
  },
]; 