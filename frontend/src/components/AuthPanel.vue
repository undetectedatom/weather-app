<template>
  <div class="overlay-shell" @click.self="$emit('close')">
    <section class="auth-panel panel" :class="mode">
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

        <button type="submit" :disabled="loading">{{ loading ? 'Please wait...' : (mode === 'signin' ? 'Sign In' : 'Register') }}</button>
      </form>

      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

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
import { ref, watch } from 'vue'

const props = defineProps({
  mode: {
    type: String,
    required: true,
  },
  loading: {
    type: Boolean,
    default: false,
  },
  errorMessage: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['close', 'switch-mode', 'submit'])
const email = ref('')
const password = ref('')

watch(
  () => props.mode,
  () => {
    password.value = ''
  }
)

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
  background: rgba(23, 49, 31, 0.24);
  display: flex;
  justify-content: flex-end;
  z-index: 60;
}

.panel {
  width: min(360px, 100%);
  background: #ffffff;
  border-right: 1px solid #cfd8cf;
  padding: 22px;
}

.panel.signin {
  border-top: 2px solid #7ab48a;
}

.panel.register {
  border-top: 2px solid #2f7d4b;
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
  color: #6f8174;
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
  color: #4f6754;
}

.auth-form input {
  border: 1px solid #cfd8cf;
  border-radius: 12px;
  padding: 12px 14px;
  background: white;
}

.auth-form button,
.icon-button {
  border: 1px solid #cfd8cf;
  border-radius: 12px;
  padding: 10px 14px;
  cursor: pointer;
}

.auth-form button {
  background: #2f7d4b;
  color: white;
  border-color: #7ab48a;
}

.error-message {
  margin-top: 14px;
  color: #a63a3a;
}

.icon-button,
.link-button {
  background: #ffffff;
  color: #23402e;
}

.switcher {
  margin-top: 18px;
  color: #4f6754;
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
