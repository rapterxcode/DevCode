export interface FooterLink {
  id: number;
  name: string;
  url: string;
}

export interface FooterSection {
  id: number;
  title: string;
  links: FooterLink[];
}

export interface SocialLink {
  id: number;
  name: string;
  icon: string;
  url: string;
}

export interface FooterData {
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

export const footerData: FooterData = {
  brand: {
    name: "BookHaven",
    icon: "📚",
    description: "Your premier destination for books, connecting readers with stories that inspire, educate, and entertain."
  },
  sections: [
    {
      id: 1,
      title: "Shop",
      links: [
        { id: 1, name: "New Releases", url: "#" },
        { id: 2, name: "Bestsellers", url: "#" },
        { id: 3, name: "Fiction", url: "#" },
        { id: 4, name: "Non-Fiction", url: "#" }
      ]
    },
    {
      id: 2,
      title: "Support",
      links: [
        { id: 1, name: "Help Center", url: "#" },
        { id: 2, name: "Shipping Info", url: "#" },
        { id: 3, name: "Returns", url: "#" },
        { id: 4, name: "Contact Us", url: "#" }
      ]
    }
  ],
  socialLinks: [
    { id: 1, name: "Facebook", icon: "📘", url: "#" },
    { id: 2, name: "Instagram", icon: "📷", url: "#" },
    { id: 3, name: "Twitter", icon: "🐦", url: "#" },
    { id: 4, name: "Email", icon: "📧", url: "#" }
  ],
  socialDescription: "Follow us for book recommendations and literary news",
  copyright: "© 2024 BookHaven. All rights reserved. | Privacy Policy | Terms of Service"
}; 