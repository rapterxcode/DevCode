interface TitleLinkProps {
    isHighlight?: boolean;
    title: string;
    link?: string;
}

const TitleLink: React.FC<TitleLinkProps> = ({isHighlight, title, link}) => {
    
    if (!link) {
        return (
            <div className={`text-primaryTitle text-1xl font-medium ${isHighlight ? "text-primaryTitleHover" : ""}`}>
                {title}
            </div>
        )
    }

    return (
        <a href={link} target="_blank">
        <div className={`text-primaryTitle text-1xl font-medium ${isHighlight ? "text-primaryTitleHover" : ""}`}>
            {title}
        </div>
        </a>
    )
}

export default TitleLink;