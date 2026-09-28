with open('src/router/index.ts', 'r', encoding='utf-8') as f:
    c = f.read()

# The localStorage stores: { token: "...", user: { role: "merchant" | "consumer" } }
# The guard was checking user.type === 'COMERCIANTE' which never matches

c = c.replace(
    "user = JSON.parse(userStr)",
    "const parsed = JSON.parse(userStr)\n      user = parsed.user || parsed"
)

c = c.replace(
    "user.type === 'COMERCIANTE'",
    "user.role === 'merchant'"
).replace(
    "user.type !== 'COMERCIANTE'",
    "user.role !== 'merchant'"
)

with open('src/router/index.ts', 'w', encoding='utf-8') as f:
    f.write(c)
