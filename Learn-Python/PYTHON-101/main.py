def calculate_grade(score):
    """
    คำนวณเกรดจากคะแนนที่ได้รับ
    Calculate letter grade based on numerical score
    
    ฟังก์ชันนี้จะรับคะแนนเป็นตัวเลขและแปลงเป็นเกรดตัวอักษร
    This function takes a numerical score and converts it to a letter grade
    
    เกณฑ์การตัดเกรด (Grading Scale):
    - A: 80-100 คะแนน
    - B: 70-79 คะแนน  
    - C: 60-69 คะแนน
    - D: 50-59 คะแนน
    - F: 0-49 คะแนน
    
    Parameters:
        score (int): คะแนนที่ต้องการแปลงเป็นเกรด (0-100)
                    The score to be converted to grade (0-100)
    
    Returns:
        str: เกรดตัวอักษร (A, B, C, D, หรือ F)
             Letter grade (A, B, C, D, or F)
    
    Examples:
        >>> calculate_grade(85)
        'A'
        >>> calculate_grade(72)
        'B'
        >>> calculate_grade(45)
        'F'
    """
    # ตรวจสอบคะแนนและตัดเกรด
    if score >= 80:
        grade = 'A'
    elif score >= 70:
        grade = 'B'
    elif score >= 60:
        grade = 'C'
    elif score >= 50:
        grade = 'D'
    else:
        grade = 'F'
    
    return grade

# function หลักเพื่อเรียกใช้และแสดงผล
def main():
    """
    ฟังก์ชันหลักสำหรับการทำงานของโปรแกรมคำนวณเกรด
    Main function for the grade calculation program
    
    ฟังก์ชันนี้เป็นจุดเริ่มต้นของโปรแกรม จะทำหน้าที่:
    This function serves as the entry point and performs:
    
    1. รับข้อมูลคะแนนจากผู้ใช้
       Accept score input from user
    
    2. เรียกใช้ฟังก์ชัน calculate_grade() เพื่อคำนวณเกรด
       Call calculate_grade() function to calculate the grade
    
    3. แสดงผลลัพธ์เกรดที่ได้
       Display the calculated grade result
    
    Returns:
        None: ไม่ส่งค่ากลับ แต่อาจแสดงผลลัพธ์ทางหน้าจอ
              No return value, but may display output to screen
    
    Example Usage:
        เมื่อรันโปรแกรม (When running the program):
        Enter the student's score: 85
        The grade for the score 85 is: A
    """
    # รับคะแนนจากผู้ใช้
    score = int(input("Enter the student's score: "))
    
    # เรียกใช้function  calculate_grade() เพื่อคำนวณเกรด
    grade = calculate_grade(score)
    
    # แสดงผลลัพธ์
    print(f"The grade for the score {score} is: {grade}")

# เรียกใช้function  main() เพื่อเริ่มโปรแกรม
if __name__ == "__main__":
    main()