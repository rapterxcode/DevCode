export interface SearchCategory {
  id: number;
  name: string;
  icon: string;
  description?: string;
}

export interface SearchData {
  title: string;
  subtitle: string;
  placeholder: string;
  searchButtonText: string;
  quickSearchCategories: SearchCategory[];
}

export const searchData: SearchData = {
  title: "Find Your Next Favorite Book",
  subtitle: "Discover millions of books across all genres. Search by title, author, ISBN, or explore our curated collections.",
  placeholder: "Search books, authors, ISBN, or browse categories...",
  searchButtonText: "Search",
  quickSearchCategories: [
    {
      id: 1,
      name: "Fiction",
      icon: "📚",
      description: "Imaginative stories and novels"
    },
    {
      id: 2,
      name: "Science Fiction",
      icon: "🔬",
      description: "Future worlds and technology"
    },
    {
      id: 3,
      name: "Romance",
      icon: "💕",
      description: "Love stories and passion"
    },
    {
      id: 4,
      name: "Mystery",
      icon: "🕵️",
      description: "Suspense and intrigue"
    },
    {
      id: 5,
      name: "Non-Fiction",
      icon: "📖",
      description: "Real stories and knowledge"
    },
    {
      id: 6,
      name: "Bestsellers",
      icon: "🎯",
      description: "Popular and trending books"
    }
  ]
}; 