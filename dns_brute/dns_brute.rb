#!/usr/bin/env ruby

require 'thread'
require 'optparse'
require 'resolv'

req_queue = Queue.new
res_queue = Queue.new
threads = Array.new

# Defaults
options = {
	:threads => 30,
	:depth => 3
}

OptionParser.new do |opts|
	opts.on("-t", "--threads THEADS", "Number of threads to use. (Default: #{options[:threads]})") do |v|
		options[:threads] = v.to_i
	end
	opts.on("-d", "--domain DOMAINS", "The target domain to scan.") do |v|
		options[:domain] = v
	end
	opts.on("-D", "--depth DEPTH", "The number of characters deep to go. (Default: #{options[:depth]}") do |v|
		options[:depth] = v.to_i
	end
	opts.on("-w", "--wordlist WORDLIST", "Optional dictionary list to test.") do |v|
		options[:wordlist] = v
	end
end.parse!

abort "Domain is required. Try --help for more information" if options[:domain].nil?

# Generate all hostnames and add them to the work queue
(options[:depth] + 1).times do |i|
	[*('a'..'z'), *('0'..'9')].repeated_permutation(i).map(&:join).reject {|e| e.empty? }.each do |w|
		req_queue << "#{w}.#{options[:domain]}"
	end
end

# Add a dictionary if we are also doing that
unless options[:wordlist].nil?
	File.read(options[:wordlist]).each_line do |line|
		req_queue << "#{line.chomp}.#{options[:domain]}"
	end
end

# Create worker threads to do our querying
options[:threads].times do
	threads << Thread.new do
		until req_queue.empty?
			begin
				req = req_queue.pop
				res_queue << "#{req},#{Resolv.getaddress(req)}"
			rescue Resolv::ResolvError => e
				# Ignore as it's just a failed query
			end
		end
	end
end

# Wait for all results to come in
threads.each { |t| t.join }

# Just print the results
until res_queue.empty?
	puts res_queue.pop
end
