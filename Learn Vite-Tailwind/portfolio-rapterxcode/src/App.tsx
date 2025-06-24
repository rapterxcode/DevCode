import './App.css'

import LeftSection from './sections/LelfSection'
import RightSection from './sections/RightSection'
import { useState, useEffect } from 'react'

interface NavItem {
  title: string;
  sectionId: string;
}

function App() {
  const [sectionIds, setSectionIds] = useState<string[]>([]);
  const [navBarItems, setNavBarItems] = useState<NavItem[]>([]);
  const [currentSection, setCurrentSection] = useState<string>("");

  const addSectionId = (sectionId: string) => {
    //console.log(sectionId);
    const elementId = document.getElementById(sectionId)?.id;
    if (elementId) {
      setSectionIds((prev) => [...new Set([...prev, elementId])]);
    }
    //console.log("sectionIds:",sectionIds);
    const elementTitle = document.getElementById(sectionId)?.childNodes[0].textContent;
    //console.log("elementTitle:",elementTitle);
    if (elementTitle && elementId) {
      const obj: NavItem = {title: elementTitle, sectionId: elementId};
      setNavBarItems((prev) => {
        if(prev.findIndex(e => e.title === obj.title) < 0) {
          return [...prev, obj];
        }
        return prev;
      });
    }
    //console.log("navBarItems:",navBarItems);
  }

  const handleScroll = () => {
    for (let index = 0; index < sectionIds.length; index++) {
      const el = sectionIds[index];
      console.log("scroll",el);
      const element = document.getElementById(el);
      if (element) {
        const eloffsetTop = element.getClientRects()[0].y;
        const height = element.getClientRects()[0].height*0.5;
        const viewHeight = window.innerHeight * 0.3;

      
        if(eloffsetTop <= 0){
          if((eloffsetTop + height) > viewHeight){
            setCurrentSection(el);
          }
        } else if(eloffsetTop > 0 && eloffsetTop < viewHeight){
          setCurrentSection(el);
        }
      }
    }
  }


  //console.log(sectionIds);
  useEffect(() => {
    if (sectionIds.length > 0) {
     // console.log("sectionIds_useEffect:",sectionIds[0]);
      setCurrentSection(sectionIds[0]);
    }
  },[sectionIds])


  useEffect(() => {
    window.addEventListener("scroll", handleScroll);
    return () => {
      window.removeEventListener("scroll", handleScroll);
    }
  },[sectionIds])

  return (
    <div className='mt-14 mx-auto max-w-7xl grid gap-y-5 lg:grid-cols-[30%_70%]'>
      <LeftSection navBarItems={navBarItems} currentSection={currentSection} />  
      <RightSection onInit={addSectionId} />
    </div>
  )
}

export default App
