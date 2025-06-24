interface FormattedDateProps {
    children: React.ReactNode;
    isHighlight?: boolean;
}

const FormattedDate: React.FC<FormattedDateProps> = ({children, isHighlight}) => {
    if (!children) return null;
    return (
        <div>
            <span className={`font-bold text-sm text-primaryContent ${isHighlight ? "text-primaryTitle" : ""}`}>
                {children}
            </span>
        </div>
    )
}

export default FormattedDate;