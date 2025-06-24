interface FormattedDateProps {
    children: React.ReactNode;
    isHighlight?: boolean;
}

const FormattedDate: React.FC<FormattedDateProps> = ({children, isHighlight}) => {
    if (!children) return null;
    return (
        <div>
            <span className={`font-bold text-sm text-mainText ${isHighlight ? "text-mainTextHover" : ""}`}>
                {children}
            </span>
        </div>
    )
}

export default FormattedDate;