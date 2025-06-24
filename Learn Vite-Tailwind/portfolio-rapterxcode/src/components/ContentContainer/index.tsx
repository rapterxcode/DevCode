import { useState, useEffect } from "react";
import Description from "../Description";
import FormattedDate from "../FormattedDate";
import Picture from "../Picture";
import TitleLink from "../TitleLink";
import Tech from "../Tech";

interface MouseEnterState {
    [key: string]: boolean;
}

/* 
<ContentContainer
    title = ""
    data={[]}

/>
*/
interface ContentContainerProps {
    title: string;
    data: any[];
    onInit?: (sectionId: string) => void;
}

const ContentContainer: React.FC<ContentContainerProps> = ({
    title: sectionTitle = "", data = [], onInit}) => {
    const [isMouseEnter, setIsMouseEnter] = useState<MouseEnterState>({});

    const SECTION_ID = `${sectionTitle}-section`;

    useEffect(() => {
        if (onInit) {
            onInit(SECTION_ID);
        }
    }, []);

    return (
        <div id={SECTION_ID} className="scroll-m-14">
            <div className="px-5">
            <div className="text-mainText text-2xl font-medium">{sectionTitle}</div>
            </div>
            
            {/* Experience 1 */}
            {
                data.map(({
                    date ="",
                    title ="",
                    link ="", 
                    description =[], 
                    tech =[], 
                    picture ="", 
                    titlePicture =""
                    }, index) => (
                    <div 
                    key={`${SECTION_ID}-${index}-${title.replace(" ", "-")}`}
                    className={`grid grid-cols-[30%_70%] gap-x-5 px-5 py-5 rounded-md transition-all duration-300 ${isMouseEnter[`${SECTION_ID}-${index}`] ? "bg-mainContainerBgHover" : ""}`} 
                    onMouseEnter={() => setIsMouseEnter({[`${SECTION_ID}-${index}`]: true})} 
                    onMouseLeave={() => setIsMouseEnter({[`${SECTION_ID}-${index}`]: false})}>
                    <div>
                        <FormattedDate isHighlight={isMouseEnter[`${SECTION_ID}-${index}`]}>{date}</FormattedDate>
                        <Picture picture={picture} title={titlePicture} />
                    </div>
                    <div className="grid gap-y-2">
                        <TitleLink isHighlight={isMouseEnter[`${SECTION_ID}-${index}`]} title={title} link={link} />
                        {
                            description.map((e: string, i: number) => (
                                <Description key={`${e}-description-${i}`} myDescription={e} />
                            ))
                        }
                        
                        {
                            tech.map((e: string[], i: number) => (
                                <Tech key={`${e}-tech-${i}`} isHighlight={isMouseEnter[`${SECTION_ID}-${index}`]} data={e} />
                            ))
                        }
                    </div>
                </div>
                ))
            }
            


        </div>
    )
}

export default ContentContainer;





