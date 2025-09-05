import streamlit as st
import numpy as np

st.set_page_config(page_title="Matrix Operations Tool", layout="centered")
st.title("🧮 Matrix Operations Tool")

st.write("Welcome to the Matrix Operations Tool! This app lets you **learn** and **practice** matrix operations step by step if you're a beginner, or directly use a **calculator** if you're experienced.")

# ---------------- Utility ----------------
def parse_matrix(input_str):
    try:
        rows = input_str.strip().split("\n")
        matrix = [list(map(float, row.split())) for row in rows]
        if len(set(len(r) for r in matrix)) != 1:
            st.error("❌ Invalid format: all rows must have the same number of elements.")
            return None
        return np.array(matrix)
    except:
        st.error("❌ Invalid matrix format. Please enter rows separated by newlines and numbers separated by spaces.")
        return None

# ---------------- Mode ----------------
mode = st.radio("Are you familiar with matrix operations?", 
                ["Beginner (Step-by-step Learning)", "Experienced (Calculator Only)"])

# ---------------- Beginner Mode ----------------
if mode.startswith("Beginner"):
    st.markdown("### 📘 Progressive Learning Path")
    level = st.selectbox("Choose your level:", [
        "Level 1: Addition & Subtraction",
        "Level 2: Multiplication",
        "Level 3: Transpose, Determinant & Inverse",
        "Level 4: Rank, Eigenvalues & Eigenvectors"
    ])

    # Learning Notes
    if level == "Level 1: Addition & Subtraction":
        st.info("📖 **Concept:** You can add or subtract matrices **only if they have the same shape**. Each element is added/subtracted individually.")
    elif level == "Level 2: Multiplication":
        st.info("📖 **Concept:** Multiply a row of A with a column of B. Requires that columns of A = rows of B.")
    elif level == "Level 3: Transpose, Determinant & Inverse":
        st.info("📖 **Concepts:**\n- **Transpose:** Flip rows and columns.\n- **Determinant:** Number describing matrix properties.\n- **Inverse:** Exists only for square matrices with nonzero determinant.")
    elif level == "Level 4: Rank, Eigenvalues & Eigenvectors":
        st.info("📖 **Concepts:**\n- **Rank:** Number of independent rows/columns.\n- **Eigenvalues & Eigenvectors:** Special numbers/vectors showing stretching behavior of the matrix.")

# ---------------- Input Guide ----------------
st.subheader("✍️ Enter Matrices")
st.caption("Enter rows separated by newlines and numbers separated by spaces. Example:\n```\n1 2 3\n4 5 6\n```")

matrix_a_str = st.text_area("Matrix A", "1 2 3\n4 5 6")
matrix_b_str = st.text_area("Matrix B", "7 8 9\n10 11 12")

A = parse_matrix(matrix_a_str)
B = parse_matrix(matrix_b_str)

if A is not None:
    st.write("### Matrix A:")
    st.write(A)
if B is not None:
    st.write("### Matrix B:")
    st.write(B)

# ---------------- Operations ----------------
if mode.startswith("Experienced"):
    operation = st.selectbox("Choose Operation", [
        "Addition (A + B)", "Subtraction (A - B)", "Multiplication (A × B)",
        "Transpose (Aᵀ, Bᵀ)", "Determinant (det(A), det(B))",
        "Inverse (A⁻¹, B⁻¹)", "Rank (rank(A), rank(B))",
        "Eigenvalues & Eigenvectors"
    ])
else:
    # Progressive operations based on level
    if level == "Level 1: Addition & Subtraction":
        operation = st.selectbox("Choose Operation", ["Addition (A + B)", "Subtraction (A - B)"])
    elif level == "Level 2: Multiplication":
        operation = "Multiplication (A × B)"
    elif level == "Level 3: Transpose, Determinant & Inverse":
        operation = st.selectbox("Choose Operation", ["Transpose (Aᵀ, Bᵀ)", "Determinant (det(A), det(B))", "Inverse (A⁻¹, B⁻¹)"])
    elif level == "Level 4: Rank, Eigenvalues & Eigenvectors":
        operation = st.selectbox("Choose Operation", ["Rank (rank(A), rank(B))", "Eigenvalues & Eigenvectors"])

# Step-by-step explanation for beginners
show_steps = False
if mode.startswith("Beginner"):
    show_steps = st.checkbox("Show step-by-step explanation")

# ---------------- Results ----------------
if A is not None and B is not None:
    st.subheader("📊 Result")
    try:
        if operation == "Addition (A + B)":
            if A.shape == B.shape:
                result = A + B
                if show_steps:
                    for i in range(A.shape[0]):
                        st.write(f"Row {i+1}: {A[i]} + {B[i]} = {result[i]}")
                st.success("✅ Result:")
                st.write(result)
            else:
                st.error("❌ Matrices must have the same shape for addition.")

        elif operation == "Subtraction (A - B)":
            if A.shape == B.shape:
                result = A - B
                if show_steps:
                    for i in range(A.shape[0]):
                        st.write(f"Row {i+1}: {A[i]} - {B[i]} = {result[i]}")
                st.success("✅ Result:")
                st.write(result)
            else:
                st.error("❌ Matrices must have the same shape for subtraction.")

        elif operation == "Multiplication (A × B)":
            if A.shape[1] == B.shape[0]:
                result = A @ B
                if show_steps:
                    for i in range(A.shape[0]):
                        for j in range(B.shape[1]):
                            st.write(f"Element C[{i+1},{j+1}] = {A[i]} · {B[:,j]} = {result[i,j]}")
                st.success("✅ Result:")
                st.write(result)
            else:
                st.error(f"❌ Cannot multiply: A is {A.shape}, B is {B.shape}. Columns of A must equal rows of B.")

        elif operation == "Transpose (Aᵀ, Bᵀ)":
            st.write("**Aᵀ:**")
            st.write(A.T)
            st.write("**Bᵀ:**")
            st.write(B.T)

        elif operation == "Determinant (det(A), det(B))":
            if A.shape[0] == A.shape[1]:
                st.write(f"det(A) = {np.linalg.det(A):.2f}")
            else:
                st.warning("Matrix A must be square to calculate determinant.")
            if B.shape[0] == B.shape[1]:
                st.write(f"det(B) = {np.linalg.det(B):.2f}")
            else:
                st.warning("Matrix B must be square to calculate determinant.")

        elif operation == "Inverse (A⁻¹, B⁻¹)":
            if A.shape[0] == A.shape[1]:
                try:
                    st.write("A⁻¹:")
                    st.write(np.linalg.inv(A))
                except np.linalg.LinAlgError:
                    st.warning("Matrix A is not invertible.")
            else:
                st.warning("Matrix A must be square to calculate inverse.")
            if B.shape[0] == B.shape[1]:
                try:
                    st.write("B⁻¹:")
                    st.write(np.linalg.inv(B))
                except np.linalg.LinAlgError:
                    st.warning("Matrix B is not invertible.")
            else:
                st.warning("Matrix B must be square to calculate inverse.")

        elif operation == "Rank (rank(A), rank(B))":
            st.write(f"rank(A) = {np.linalg.matrix_rank(A)}")
            st.write(f"rank(B) = {np.linalg.matrix_rank(B)}")

        elif operation == "Eigenvalues & Eigenvectors":
            if A.shape[0] == A.shape[1]:
                vals, vecs = np.linalg.eig(A)
                st.write("Eigenvalues of A:")
                st.write(vals)
                st.write("Eigenvectors of A:")
                st.write(vecs)
            else:
                st.warning("Matrix A must be square to calculate eigenvalues.")
            if B.shape[0] == B.shape[1]:
                vals, vecs = np.linalg.eig(B)
                st.write("Eigenvalues of B:")
                st.write(vals)
                st.write("Eigenvectors of B:")
                st.write(vecs)
            else:
                st.warning("Matrix B must be square to calculate eigenvalues.")

    except Exception as e:
        st.error(f"⚠️ Error performing operation: {e}")
