import { faArrowRight } from "@fortawesome/free-solid-svg-icons"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { useState } from "react";

interface MouseEnterState {
    [key: string]: boolean;
}

interface NavItem {
  title: string;
  sectionId: string;
}

interface NavbarProps {
  navBarItems: NavItem[];
  currentSection: string;
}

const Navbar: React.FC<NavbarProps> = ({ navBarItems, currentSection }) => {

    const [isMouseEnter, setIsMouseEnter] = useState<MouseEnterState>({});

    const handleClick = (sectionId: string) => {
      //console.log(sectionId);
      document.getElementById(sectionId)?.scrollIntoView({behavior: "smooth"});
    }
    //console.log("currentSection:",currentSection);
    return (
        <div className='flex flex-col gap-3 font-semibold text-mainText mt-6'>
             {
              navBarItems.map((e, i) => (
                <div key={`nav-${e.title}-${i}`}
                onClick={() => handleClick(e.sectionId)}
                onMouseEnter={() => setIsMouseEnter({ [e.title]: true})}
                onMouseLeave={() => setIsMouseEnter({ [e.title]: false})}
                className="cursor-pointer flex"
                >
                  <FontAwesomeIcon 
                  className={`mr-2  ${currentSection === e.sectionId ? "text-mainIconBg" : isMouseEnter[e.title] ? "text-mainIconBg" : "opacity-0"}`} icon={faArrowRight} 
                  />
                  <div className={`${currentSection === e.sectionId || isMouseEnter[e.title] ? "translate-x-2" : ""} transition-all duration-500`}>{e.title}</div>
                </div>
              ))
             }
        </div>
    )   
}

export default Navbar;