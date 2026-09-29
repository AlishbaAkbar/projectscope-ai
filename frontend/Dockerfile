# Install dependencies and compile the standalone Next.js application.
FROM node:20-alpine AS builder

WORKDIR /app

# Use the committed lockfile for a reproducible dependency install.
COPY package*.json ./
RUN npm ci

# Build the application with standalone output enabled in Next config.
COPY . .
RUN npm run build

# Run the standalone server in a smaller production image.
FROM node:20-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# Copy only the files required by Next.js standalone production output.
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

# Use an unprivileged account for the production server.
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001 && \
    chown -R nextjs:nodejs /app
USER nextjs

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]
