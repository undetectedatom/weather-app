<template>
  <div class="overlay-shell" @click.self="$emit('close')">
    <section class="auth-panel panel">
      <div class="panel-header">
        <div>
          <p class="eyebrow">Account</p>
          <h2 v-if="mode === 'signin'">Sign in</h2>
          <h2 v-else>Register</h2>
        </div>
        <button class="icon-button" type="button" @click="$emit('close')">Close</button>
      </div>

      <form class="auth-form" @submit.prevent="submitAuth">
        <label>
          <span>Email</span>
          <input v-model="email" type="email" placeholder="name@example.com" />
        </label>

        <label>
          <span>Password</span>
          <input v-model="password" type="password" placeholder="••••••••" />
        </label>

        <button type="submit">{{ mode === 'signin' ? 'Sign In' : 'Register' }}</button>
      </form>

      <div class="switcher">
        <p v-if="mode === 'signin'">
          Don't have an account?
          <button type="button" class="link-button" @click="$emit('switch-mode', 'register')">Register</button>
        </p>
        <p v-else>
          Already have an account?
          <button type="button" class="link-button" @click="$emit('switch-mode', 'signin')">Sign In</button>
        </p>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  mode: {
    type: String,
    required: true,
  },
})

const emit = defineEmits(['close', 'switch-mode', 'submit'])
const email = ref('')
const password = ref('')

function submitAuth() {
  emit('submit', {
    mode: props.mode,
    email: email.value,
    password: password.value,
  })
}
</script>

<style scoped>
.overlay-shell {
  position: fixed;
  inset: 0;
  background: rgba(8, 15, 28, 0.32);
  display: flex;
  justify-content: flex-end;
  z-index: 60;
}

.panel {
  width: min(360px, 100%);
  background: rgba(255, 255, 255, 0.97);
  border-right: 1px solid rgba(16, 35, 63, 0.08);
  box-shadow: 18px 0 50px rgba(16, 35, 63, 0.14);
  padding: 22px;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
  margin-bottom: 18px;
}

.eyebrow {
  margin: 0 0 4px;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.16em;
  color: #5f7392;
}

h2,
p {
  margin: 0;
}

.auth-form {
  display: grid;
  gap: 14px;
}

.auth-form label {
  display: grid;
  gap: 6px;
  color: #4f6786;
}

.auth-form input {
  border: 1px solid rgba(16, 35, 63, 0.12);
  border-radius: 14px;
  padding: 12px 14px;
  background: white;
}

.auth-form button,
.icon-button {
  border: 0;
  border-radius: 14px;
  padding: 10px 14px;
  cursor: pointer;
}

.auth-form button {
  background: linear-gradient(135deg, #1d4ed8, #38bdf8);
  color: white;
}

.icon-button,
.link-button {
  background: #eef4ff;
  color: #21416f;
}

.switcher {
  margin-top: 18px;
  color: #4f6786;
}

.link-button {
  border: 0;
  padding: 0;
  cursor: pointer;
  font: inherit;
  text-decoration: underline;
}

@media (max-width: 640px) {
  .overlay-shell {
    justify-content: stretch;
  }

  .panel {
    width: 100%;
    min-height: 100%;
    border-right: 0;
  }
}
</style>
