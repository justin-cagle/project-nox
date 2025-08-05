import { render, screen } from '@testing-library/react';
import { RegistrationForm } from '../RegistrationForm'
import { expect } from 'vitest'

describe('RegistrationForm', () => {
  it('renders without crashing', () => {
    render(<RegistrationForm />);

    expect(
      screen.getByRole('heading', { name: /create/i })
    ).toBeInTheDocument();
  });

  it('email textbox renders', () => {
    render(<RegistrationForm />);

    expect(
      screen.getByRole('textbox', { name: /email/i })
    ).toBeInTheDocument()
  });

  it('username textbox renders', () => {
    render(<RegistrationForm />);

    expect(
      screen.getByRole('textbox', { name: /username/i })
    ).toBeInTheDocument()
  });

  it('display name textbox renders', () => {
    render(<RegistrationForm />);

    expect(
      screen.getByRole('textbox', { name: /display/i })
    ).toBeInTheDocument()
  });

  it('password textbox renders', () => {
    render(<RegistrationForm />);
    const passwordInput = screen.getByLabelText(/^password$/i)
    expect(passwordInput).toBeInTheDocument()
  });

  it('second password textbox renders', () => {
    render(<RegistrationForm />);
    const passwordInput = screen.getByLabelText(/confirm password/i)
    expect(passwordInput).toBeInTheDocument()
  });

  it('submit button renders', () => {
    render(<RegistrationForm />);

    expect(screen.getByRole('button', { name: /register/i })
    ).toBeInTheDocument()
  });
});
