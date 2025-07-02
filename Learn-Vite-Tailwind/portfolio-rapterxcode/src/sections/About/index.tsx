import { data } from "../../contents/about";
import { useEffect } from "react";

interface AboutProps {
    onInit?: (sectionId: string) => void;
    title: string;
}

const About: React.FC<AboutProps> = ({ onInit , title}) => {
    const SECTION_ID = `${title}-section`;

    useEffect(() => {
        if (onInit) {
            onInit(SECTION_ID);
        }
    }, []);

    return (
        
        <div className="space-y-5 mb-30 px-5 scroll-m-14" id={SECTION_ID}>
            <div className="text-mainText text-2xl font-medium">{data.title}</div>
            <div className="text-mainText">{data.description}</div>
        </div>
        
    )
}

export default About;