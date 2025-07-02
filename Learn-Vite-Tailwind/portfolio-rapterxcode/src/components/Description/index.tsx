interface DescriptionProps {
    myDescription: string;
}

const Description: React.FC<DescriptionProps> = ({myDescription}) => {
    if (!myDescription) return null;
    return (
        <div className="text-mainText text-sm">{myDescription}</div>
    )
}

export default Description;