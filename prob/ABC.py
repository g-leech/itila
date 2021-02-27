import itertools
import random
import matplotlib.pyplot as plt


n_visitors_a = 100  # number of visitors shown layout A
n_conv_a = 4        # number of As who converted

n_visitors_b = 40
n_conv_b = 2

def posterior_sampler(data, prior_sampler, simulate):
    '''Yield samples from the posterior by ABC.'''
    
    for p in prior_sampler:
        s = simulate(p)
        if s == data:
            yield p



def simulate(p, n):
    '''Return #visitors who convert, given CR p.'''
    outcomes = (random.random() < p for i in range(n))
    return sum(outcomes)


def take(n, iterable):
    return list(itertools.islice(iterable, n))


# Perfect ignorance
def uniform_prior_sampler():
    '''Yield random numbers in interval (0, 1).'''
    while True:
        yield random.random()


def normal_prior_sampler(mu=0.06, sigma=0.02):
    '''Yield stream of samples from N(mu, sigma) in interval (0, 1).'''
    while True:
        x = random.normalvariate(mu, sigma)
        if 0 <= x <= 1:
            yield x






m = 20000
a_samples = take(m, uniform_prior_sampler())
b_samples = take(m, normal_prior_sampler())


# What's the probability that the real A conv is 10%?
print( sum(a > 0.1 for a in a_samples)/len(a_samples) )

# Plot priors
abbins = [i/200.0 for i in range(50)]          # 50 bins between 0 and 0.25
plt.hist(a_samples, bins=abbins, label='A', density = True)
plt.hist(b_samples, bins=abbins, label='B', alpha=0.5, density = True)
plt.title('Prior distributions')
plt.xlim(0, max(abbins))
plt.legend();
plt.show()

# Plot posteriors
posterior_a_sampler = posterior_sampler(
    data=n_conv_a,
    prior_sampler=uniform_prior_sampler(),
    simulate=lambda p: simulate(p, n_visitors_a)
)

posterior_b_sampler = posterior_sampler(
    data=n_conv_b,
    prior_sampler=normal_prior_sampler(),
    simulate=lambda p: simulate(p, n_visitors_b)
)

a_samples = take(m, posterior_a_sampler)
b_samples = take(m, posterior_b_sampler)

plt.hist(a_samples, bins=abbins, label='A', density = True)
plt.hist(b_samples, bins=abbins, label='B', alpha=0.5, density = True)
plt.title('Posterior distributions')
plt.xlim(0, max(abbins));
plt.legend();
plt.show()


# Money shot

def p_b_greater_than_a(as_, bs) :
	greaters = sum(b > a for a, b in zip(as_, bs))
	n = len(a_samples)
	return greaters/n

print(p_b_greater_than_a(a_samples, b_samples))