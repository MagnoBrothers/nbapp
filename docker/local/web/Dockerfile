# Install dependencies only when needed
FROM node:16-alpine

ENV NODE_ENV development
ENV NEXT_TELEMETRY_DISABLED 1

# Check https://github.com/nodejs/docker-node/tree/b4117f9333da4138b03a546ec926ef50a31506c3#nodealpine to understand why libc6-compat might be needed.
RUN apk add --no-cache libc6-compat
WORKDIR /nbweb

# Install dependencies based on the preferred package manager
COPY ./nbweb/package.json ./nbweb/package-lock.json* ./
RUN npm ci

# RUN addgroup --system --gid 1001 nodejs
# RUN adduser --system --uid 1001 nextjs

# USER nextjs

EXPOSE 3000

ENV PORT 3000

CMD ["npm", "run", "dev"]
