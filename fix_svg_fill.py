import re

files = [
    'src/views/auth/LoginView.vue',
    'src/views/auth/RegisterView.vue',
    'src/views/auth/ForgotPasswordView.vue',
    'src/views/auth/ResetPasswordView.vue'
]

for file_path in files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            c = f.read()

        # Add inline fill to the path if missing
        # The path starts with <path d="M7 18
        c = re.sub(r'(<path d="M7 18[^>]+?)"\s*/>', r'\1" fill="#FF3B69" />', c)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"Fixed {file_path}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
