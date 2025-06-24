interface TechProps {
    isHighlight?: boolean;
    data: string[];
}

const Tech: React.FC<TechProps> = ({isHighlight, data}) => {
    if (!data) return null;
    return (
        <div className="flex flex-wrap gap-2">
            {
                data.map((e, i) => (
                    <div key={`${e}-${i}`} className={`text-primaryContent text-sm bg-primaryBg rounded-md px-2 py-1 ${isHighlight ? "text-primaryContentHover" : ""}`}>
                        {e}
                    </div>
                ))
            }

        </div>
    )
}

export default Tech;