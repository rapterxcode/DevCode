export interface HeaderButton {
  id: number;
  icon: string;
  label: string;
  action?: () => void;
  badge?: number;
  type: 'navigation' | 'action' | 'auth';
}

export interface HeaderData {
  brand: {
    name: string;
    icon: string;
  };
  navigationButtons: HeaderButton[];
  actionButtons: HeaderButton[];
  authButtons: HeaderButton[];
}

export const headerData: HeaderData = {
  brand: {
    name: "BookHaven",
    icon: "📚"
  },
  navigationButtons: [
    {
      id: 1,
      icon: "🏠",
      label: "Home",
      type: "navigation"
    }
  ],
  actionButtons: [
    {
      id: 1,
      icon: "📖",
      label: "Wishlist",
      type: "action"
    },
    {
      id: 2,
      icon: "🛒",
      label: "Cart",
      type: "action",
      badge: 3
    }
  ],
  authButtons: [
    {
      id: 1,
      label: "Sign In",
      icon: "",
      type: "auth"
    },
    {
      id: 2,
      label: "Join Now",
      icon: "",
      type: "auth"
    }
  ]
}; 