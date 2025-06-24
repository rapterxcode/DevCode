interface TitleLinkProps {
    isHighlight?: boolean;
    title: string;
    link?: string;
}

const TitleLink: React.FC<TitleLinkProps> = ({isHighlight, title, link}) => {
    
    if (!link) {
        return (
            <div className={`text-mainText text-1xl font-medium ${isHighlight ? "text-mainTextHover" : ""}`}>
                {title}
            </div>
        )
    }

    return (
        <a href={link} target="_blank">
        <div className={`text-mainText text-1xl font-medium ${isHighlight ? "text-mainTextHover" : ""}`}>
            {title}
        </div>
        </a>
    )
}

export default TitleLink;